from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.schemas.template import TemplateStatus, TemplateType


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    html_content = Column(Text, nullable=False)
    css_content = Column(Text, nullable=True)
    js_content = Column(Text, nullable=True)
    config = Column(JSON, nullable=True)
    type = Column(SQLEnum(TemplateType), default=TemplateType.DASHBOARD)
    status = Column(SQLEnum(TemplateStatus), default=TemplateStatus.DRAFT)
    tags = Column(JSON, nullable=True)  # Store as JSON array
    parent_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    version_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now)
    created_by = Column(Integer, nullable=True)  # User ID reference
    updated_by = Column(Integer, nullable=True)  # User ID reference
    version = Column(Integer, default=1)

    # Relationships
    parent = relationship("Template", remote_side=[id], backref="children")
    routes = relationship("Route", back_populates="template")

    def __repr__(self):
        return f"<Template {self.name} (v{self.version})>"
