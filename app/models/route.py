from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(200), unique=True, nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    method = Column(String(10), default="GET")
    handler_config = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    access_count = Column(Integer, default=0)

    # Relationships
    template = relationship("Template", back_populates="routes")

    def __repr__(self):
        return f"<Route {self.method} {self.path}>" 