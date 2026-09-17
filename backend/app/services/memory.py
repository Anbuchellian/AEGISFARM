from datetime import datetime
from sqlalchemy.orm import Session
from ..models.entities import ResponseMemory


def choose_historical_strategy(db: Session, species: str, zone: str) -> str | None:
    rows = db.query(ResponseMemory).filter(ResponseMemory.species == species, ResponseMemory.zone == zone).all()
    if not rows:
        return None
    rows.sort(key=lambda r: (r.successes / r.attempts) if r.attempts else 0, reverse=True)
    return rows[0].strategy if rows else None


def record_outcome(db: Session, species: str, zone: str, strategy: str, success: bool, outcome: str) -> ResponseMemory:
    row = (
        db.query(ResponseMemory)
        .filter(ResponseMemory.species == species, ResponseMemory.zone == zone, ResponseMemory.strategy == strategy)
        .first()
    )
    if row is None:
        row = ResponseMemory(species=species, zone=zone, strategy=strategy)
        db.add(row)
    row.attempts = (row.attempts or 0) + 1
    row.successes = (row.successes or 0) + (1 if success else 0)
    row.last_outcome = outcome
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return row
