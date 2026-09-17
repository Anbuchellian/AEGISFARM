from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models.entities import Detection, Intervention, ResponseMemory, ValidationRecord
from ..schemas import DetectionOut, InterventionOut, ValidationCreate, ValidationOut, EventScenario
from ..services.detection import AnimalDetector
from ..config import settings
from ..services.risk import assess_risk
from ..services.response_engine import select_strategy, adaptive_retry, close_loop
from ..services.observation import verify_retreat

router = APIRouter(prefix="/api", tags=["AEGISFARM"])

detector = AnimalDetector(settings.model_path)


def _dashboard(db: Session):
    latest = db.query(Detection).order_by(Detection.detected_at.desc()).first()
    total = db.query(Detection).count()
    active = db.query(Intervention).filter(Intervention.outcome == "pending").count()
    successes = db.query(Intervention).filter(Intervention.outcome == "retreated").count()
    response_rows = db.query(ResponseMemory).all()
    return {
        "farm": {"status": "PROTECTED", "name": "AEGISFARM Demo Farm", "nodes_online": 3},
        "stats": {
            "total_intrusions": total,
            "active_interventions": active,
            "verified_retreats": successes,
            "response_memory_entries": len(response_rows),
        },
        "latest_detection": DetectionOut.model_validate(latest).model_dump() if latest else None,
        "zones": [
            {"id": "Z1", "name": "North-West", "risk": 78},
            {"id": "Z2", "name": "North-East", "risk": 36},
            {"id": "Z3", "name": "South-West", "risk": 58},
            {"id": "Z4", "name": "South-East", "risk": 24},
        ],
    }


@router.get("/health")
def health():
    return {"ok": True, "service": "AEGISFARM", "mode": "prototype"}


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return _dashboard(db)


@router.get("/detections", response_model=list[DetectionOut])
def detections(db: Session = Depends(get_db)):
    return db.query(Detection).order_by(Detection.detected_at.desc()).limit(50).all()


@router.get("/interventions", response_model=list[InterventionOut])
def interventions(db: Session = Depends(get_db)):
    return db.query(Intervention).order_by(Intervention.created_at.desc()).limit(50).all()


@router.post("/simulate")
def simulate(event: EventScenario, db: Session = Depends(get_db)):
    risk = assess_risk(event.confidence, event.zone, event.direction)
    detection = Detection(
        species=event.species.replace("_", " ").title(),
        confidence=event.confidence,
        zone=event.zone,
        direction=event.direction,
        threat_state=event.threat_state,
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    plan = select_strategy(db, detection.species, event.zone, risk.level)
    intervention = Intervention(
        detection_id=detection.id,
        strategy=plan.strategy,
        outcome="pending",
        response_time_ms=320,
        notes=plan.reason,
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)

    observation = verify_retreat(event.simulate_no_response)
    if observation.outcome == "no_response":
        retry = adaptive_retry(db, detection.species, event.zone, plan.strategy)
        intervention.outcome = "no_response"
        intervention.notes += f" | Retry: {retry.strategy}"
        db.commit()

        retry_intervention = Intervention(
            detection_id=detection.id,
            strategy=retry.strategy,
            outcome="pending",
            response_time_ms=420,
            notes=retry.reason,
        )
        db.add(retry_intervention)
        db.commit()
        db.refresh(retry_intervention)

        retry_observation = verify_retreat(False)
        retry_intervention.outcome = retry_observation.outcome
        retry_intervention.notes += " | Retreat verified by simulated tracking state"
        db.commit()
        close_loop(db, detection.species, event.zone, plan.strategy, "no_response")
        close_loop(db, detection.species, event.zone, retry.strategy, retry_observation.outcome)
        return {
            "detection": DetectionOut.model_validate(detection).model_dump(),
            "risk": risk.__dict__,
            "interventions": [InterventionOut.model_validate(intervention).model_dump(), InterventionOut.model_validate(retry_intervention).model_dump()],
            "closed_loop": "ADAPTIVE_RETRY → RETREAT_CONFIRMED",
        }

    intervention.outcome = observation.outcome
    intervention.notes += " | Retreat verified by simulated tracking state"
    db.commit()
    close_loop(db, detection.species, event.zone, plan.strategy, observation.outcome)
    return {
        "detection": DetectionOut.model_validate(detection).model_dump(),
        "risk": risk.__dict__,
        "interventions": [InterventionOut.model_validate(intervention).model_dump()],
        "closed_loop": "RESPONSE_VERIFIED",
    }


@router.post("/detect/image")
async def detect_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    results = detector.infer_image(data)
    if not results:
        raise HTTPException(status_code=422, detail="No object detected")
    saved = []
    for result in results:
        detection = Detection(
            species=result.species,
            confidence=result.confidence,
            zone=result.zone,
            direction=result.direction,
            threat_state=result.threat_state,
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        saved.append(DetectionOut.model_validate(detection).model_dump())
    return {"detections": saved, "note": "If no model weights are configured, demo fallback is used."}


@router.get("/validation", response_model=list[ValidationOut])
def validation(db: Session = Depends(get_db)):
    return db.query(ValidationRecord).order_by(ValidationRecord.created_at.desc()).all()


@router.post("/validation", response_model=ValidationOut)
def add_validation(payload: ValidationCreate, db: Session = Depends(get_db)):
    row = ValidationRecord(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.post("/reset")
def reset(db: Session = Depends(get_db)):
    for model in [Detection, Intervention, ResponseMemory, ValidationRecord]:
        db.query(model).delete()
    db.commit()
    return {"reset": True}
