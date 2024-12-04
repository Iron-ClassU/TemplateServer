# API Documentation

## Overview

The Dashboard Generator API is organized around REST. The API accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes and verbs.

## Base URL

All API endpoints are prefixed with `/api/v1/`.

## Authentication

(To be implemented)

## Endpoints

### Templates

#### Create Template
```http
POST /api/v1/templates/
```

Request body:
```json
{
  "name": "string",
  "description": "string",
  "html_content": "string",
  "css_content": "string",
  "js_content": "string",
  "config": {
    "type": "dashboard|report|widget|layout",
    "layout": {},
    "theme": {},
    "components": [],
    "data_bindings": {},
    "permissions": {},
    "settings": {}
  },
  "status": "draft|published|archived",
  "tags": ["string"],
  "parent_id": "integer"
}
```

#### List Templates
```http
GET /api/v1/templates/
```

Query parameters:
- `skip` (integer): Number of records to skip
- `limit` (integer): Maximum number of records to return
- `type` (string): Filter by template type
- `status` (string): Filter by status
- `tag` (string): Filter by tag
- `search` (string): Search in name and description

### Routes

#### Create Route
```http
POST /api/v1/routes/
```

Request body:
```json
{
  "path": "string",
  "template_id": "integer",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "handler_config": {}
}
```

#### List Routes
```http
GET /api/v1/routes/
```

Query parameters:
- `skip` (integer): Number of records to skip
- `limit` (integer): Maximum number of records to return
- `template_id` (integer): Filter by template

### Data Sources

#### Create Data Source
```http
POST /api/v1/data/sources/
```

Request body:
```json
{
  "name": "string",
  "description": "string",
  "config": {
    "type": "rest_api|database|file|static",
    "connection_details": {},
    "parameters": {},
    "headers": {},
    "auth_config": {},
    "cache_ttl": "integer",
    "retry_config": {}
  },
  "transform_config": {},
  "schedule": "string"
}
```

#### Query Data Source
```http
POST /api/v1/data/sources/{id}/query
```

Request body:
```json
{
  "filters": {},
  "sort": ["string"],
  "page": "integer",
  "page_size": "integer",
  "fields": ["string"]
}
```

## Response Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Error Responses

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```

For validation errors:
```json
{
  "detail": [
    {
      "loc": ["field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
``` 