from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any
import json
import aiohttp
import asyncio
from datetime import datetime

from app.models.data import DataSource
from app.schemas.data import DataSourceCreate, DataSourceUpdate, DataQueryParams, DataQueryResult, DataValidationResult

class DataService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_data_source(self, data: DataSourceCreate) -> DataSource:
        db_data_source = DataSource(
            name=data.name,
            description=data.description,
            config=data.config.dict(),
            transform_config=data.transform_config,
            schedule=data.schedule
        )
        self.session.add(db_data_source)
        await self.session.commit()
        await self.session.refresh(db_data_source)
        return db_data_source

    async def get_data_source(self, data_source_id: int) -> Optional[DataSource]:
        result = await self.session.execute(
            select(DataSource).where(DataSource.id == data_source_id)
        )
        return result.scalars().first()

    async def get_data_sources(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[DataSource]:
        query = select(DataSource)
        
        if filter_params:
            if 'is_active' in filter_params:
                query = query.where(DataSource.is_active == filter_params['is_active'])
            if 'type' in filter_params:
                query = query.where(DataSource.config['type'].astext == filter_params['type'])
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_data_source(
        self,
        data_source_id: int,
        data: DataSourceUpdate
    ) -> Optional[DataSource]:
        update_data = data.dict(exclude_unset=True)
        if 'config' in update_data:
            update_data['config'] = update_data['config'].dict()
        
        result = await self.session.execute(
            update(DataSource)
            .where(DataSource.id == data_source_id)
            .values(**update_data)
            .returning(DataSource)
        )
        await self.session.commit()
        return result.scalars().first()

    async def delete_data_source(self, data_source_id: int) -> bool:
        result = await self.session.execute(
            delete(DataSource).where(DataSource.id == data_source_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def validate_data_source(self, data_source: DataSource) -> DataValidationResult:
        errors = []
        warnings = []
        metadata = {}

        try:
            # Validate connection based on data source type
            if data_source.config['type'] == 'rest_api':
                async with aiohttp.ClientSession() as session:
                    url = data_source.config['connection_details']['url']
                    headers = data_source.config.get('headers', {})
                    async with session.get(url, headers=headers) as response:
                        metadata['status_code'] = response.status
                        metadata['response_time'] = response.elapsed
                        if response.status >= 400:
                            errors.append({
                                'type': 'connection_error',
                                'message': f'HTTP {response.status} error'
                            })
            
            # Validate schedule if present
            if data_source.schedule:
                try:
                    # Add cron expression validation here
                    pass
                except ValueError as e:
                    errors.append({
                        'type': 'schedule_error',
                        'message': str(e)
                    })

            # Validate transform config if present
            if data_source.transform_config:
                # Add transform config validation here
                pass

        except Exception as e:
            errors.append({
                'type': 'validation_error',
                'message': str(e)
            })

        return DataValidationResult(
            is_valid=len(errors) == 0,
            errors=errors if errors else None,
            warnings=warnings if warnings else None,
            metadata=metadata
        )

    async def query_data(
        self,
        data_source_id: int,
        query_params: DataQueryParams
    ) -> DataQueryResult:
        data_source = await self.get_data_source(data_source_id)
        if not data_source:
            raise ValueError("Data source not found")

        # Execute query based on data source type
        if data_source.config['type'] == 'rest_api':
            return await self._query_rest_api(data_source, query_params)
        elif data_source.config['type'] == 'database':
            return await self._query_database(data_source, query_params)
        else:
            raise ValueError(f"Unsupported data source type: {data_source.config['type']}")

    async def _query_rest_api(
        self,
        data_source: DataSource,
        query_params: DataQueryParams
    ) -> DataQueryResult:
        url = data_source.config['connection_details']['url']
        headers = data_source.config.get('headers', {})
        
        # Build query parameters
        params = {}
        if query_params.filters:
            params.update(query_params.filters)
        if query_params.sort:
            params['sort'] = ','.join(query_params.sort)
        if query_params.page:
            params['page'] = query_params.page
        if query_params.page_size:
            params['page_size'] = query_params.page_size

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                result = await response.json()

                # Apply transformations if configured
                if data_source.transform_config:
                    result = self._apply_transformations(result, data_source.transform_config)

                return DataQueryResult(
                    data=result.get('data', []),
                    total=result.get('total', len(result.get('data', []))),
                    page=query_params.page or 1,
                    page_size=query_params.page_size or 50,
                    total_pages=result.get('total_pages', 1)
                )

    async def _query_database(
        self,
        data_source: DataSource,
        query_params: DataQueryParams
    ) -> DataQueryResult:
        # Implement database query logic here
        raise NotImplementedError("Database querying not yet implemented")

    def _apply_transformations(
        self,
        data: Dict[str, Any],
        transform_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Implement data transformation logic here
        return data

    async def sync_data_source(self, data_source_id: int) -> bool:
        data_source = await self.get_data_source(data_source_id)
        if not data_source:
            raise ValueError("Data source not found")

        try:
            # Update sync status
            data_source.sync_status = "in_progress"
            data_source.last_sync = func.now()
            await self.session.commit()

            # Perform sync based on data source type
            if data_source.config['type'] == 'rest_api':
                await self._sync_rest_api(data_source)
            elif data_source.config['type'] == 'database':
                await self._sync_database(data_source)

            # Update sync status on success
            data_source.sync_status = "completed"
            await self.session.commit()
            return True

        except Exception as e:
            # Update sync status on failure
            data_source.sync_status = f"failed: {str(e)}"
            await self.session.commit()
            raise

    async def _sync_rest_api(self, data_source: DataSource):
        # Implement REST API sync logic here
        pass

    async def _sync_database(self, data_source: DataSource):
        # Implement database sync logic here
        pass 