from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class AssetModel(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    type = Column(String(100), nullable=False)

    publishes = relationship(
        "PublishModel", back_populates="asset", cascade="all, delete-orphan"
    )
