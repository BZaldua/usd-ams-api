from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class PublishModel(Base):
    __tablename__ = "publishes"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )
    task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    version = Column(Integer, nullable=False, default=1)
    fs_path = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    author = Column(String(255), nullable=True)

    asset = relationship("AssetModel", back_populates="publishes")
    task = relationship("TaskModel", back_populates="publishes")
    variants = relationship(
        "VariantModel", back_populates="publish", cascade="all, delete-orphan"
    )

    __tableargs__ = UniqueConstraint(
        "asset_id", "task_id", "version", name="uq_asset_task_version"
    )
