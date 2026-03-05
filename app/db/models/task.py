import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    deadline_days = Column(Integer, nullable=False)
    estimated_hours = Column(Float, nullable=False)
    importance = Column(Integer, nullable=False)
    score = Column(Float, nullable=True)  # Calculated priority score
    category = Column(String, nullable=True)  # Task category

    # Foreign key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    # Relationship
    owner = relationship("UserModel", back_populates="tasks")