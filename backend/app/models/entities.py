from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base


class Detection(Base):
    __tablename__ = "detections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    species: Mapped[str] = mapped_column(String(100))
    confidence: Mapped[float] = mapped_column(Float)
    zone: Mapped[str] = mapped_column(String(50))
    direction: Mapped[str] = mapped_column(String(50), default="unknown")
    threat_state: Mapped[str] = mapped_column(String(50), default="monitoring")
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Intervention(Base):
    __tablename__ = "interventions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detection_id: Mapped[int] = mapped_column(Integer)
    strategy: Mapped[str] = mapped_column(String(100))
    outcome: Mapped[str] = mapped_column(String(50), default="pending")
    response_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ResponseMemory(Base):
    __tablename__ = "response_memory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    species: Mapped[str] = mapped_column(String(100))
    zone: Mapped[str] = mapped_column(String(50))
    strategy: Mapped[str] = mapped_column(String(100))
    successes: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_outcome: Mapped[str] = mapped_column(String(50), default="unknown")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ValidationRecord(Base):
    __tablename__ = "validation_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tester: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(150))
    task: Mapped[str] = mapped_column(String(200))
    feedback: Mapped[str] = mapped_column(Text)
    change_made: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
