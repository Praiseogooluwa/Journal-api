from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    date = Column(Date, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tags = relationship("Tag", secondary="entry_tags", backref="entries")