from datetime import datetime
import uuid

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    BigInteger
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from app.core.enums import ImageIngestionStates, UserConsentTypes
from app.core.databases import Base

from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class ImageRegistry(Base):

    __tablename__ = "image_registry"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    object_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=ImageIngestionStates.PENDING.value,
        index=True
    )

    consent_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=UserConsentTypes.NO.value
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    image_metadata = relationship(
        "ImageMetadata",
        back_populates="image_registry",
        uselist=False
    )

class ImageMetadata(Base):

    __tablename__ = "image_metadata"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    image_registry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("image_registry.id"),
        nullable=False,
        unique=True,
        index=True
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True
    )

    perceptual_hash: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True
    )

    image_width: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    image_height: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    image_registry = relationship(
        "ImageRegistry",
        back_populates="image_metadata"
    )