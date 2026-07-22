from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class VariantModel(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    publish_id = Column(
        Integer, ForeignKey("publishes.id", ondelete="CASCADE"), nullable=False
    )
    variant_set = Column(String(100), nullable=False)
    variant_name = Column(String(100), nullable=False)

    publish = relationship("PublishModel", back_populates="variants")

    __tableargs__ = UniqueConstraint(
        "publish_id", "variant_set", "variant_name", name="uq_publish_variant_set_name"
    )
