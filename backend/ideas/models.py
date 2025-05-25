from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Integer

from backend.db import Base


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(50), default="draft", nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_shared = Column(Integer, default=0, nullable=True)  # 0 for private, 1 for shared

    user = relationship("User", back_populates="ideas")
    tags = relationship("Tag", secondary="idea_tags", back_populates="ideas")
    scripts = relationship("IdeaScript", back_populates="idea", cascade="all, delete-orphan")
    comments = relationship("IdeaComment", back_populates="idea", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    ideas = relationship("Idea", secondary="idea_tags", back_populates="tags")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="tags")


class IdeaTag(Base):
    __tablename__ = "idea_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idea_id = Column(Integer, ForeignKey("ideas.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


class IdeaComment(Base):
    __tablename__ = "idea_comments"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    idea = relationship("Idea", back_populates="comments")


class IdeaScript(Base):
    __tablename__ = "idea_scripts"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    script_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    idea = relationship("Idea", back_populates="scripts")

