from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    publishes = relationship("Publish", back_populates="task")
