import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base
import enum


class RoleEnum(str, enum.Enum):
    scientist = "scientist"
    manager = "manager"
    mission_architect = "mission_architect"


class Publication(Base):
    __tablename__ = "publications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    year = Column(Integer, nullable=True)
    # mission_type = Column(String, nullable=True)   # e.g., Mars, Lunar, ISS
    # organism = Column(String, nullable=True)       # e.g., plant, human, bacteria
    journal = Column(String, nullable=True)
    date = Column(String, nullable=True)
    authors = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # relationships
    sections = relationship("PublicationSection", back_populates="publication", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="publication", cascade="all, delete-orphan")


class PublicationSection(Base):
    __tablename__ = "publication_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"))
    section_name = Column(String, nullable=False)   # Abstract, Intro, Results...
    section_text = Column(Text, nullable=False)
    section_summary = Column(Text, nullable=True)

    publication = relationship("Publication", back_populates="sections")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"))
    scientist_summary = Column(JSONB, nullable=True)
    manager_summary = Column(JSONB, nullable=True)
    mission_architect_summary = Column(JSONB, nullable=True)
      # {section_name: summary_text}
    # metadata = Column(JSONB, nullable=True)  # store extra info like version, LLM model used
    created_at = Column(TIMESTAMP, server_default=func.now())

    publication = relationship("Publication", back_populates="summaries")
