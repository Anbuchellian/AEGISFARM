from dataclasses import dataclass
from sqlalchemy.orm import Session
from .memory import choose_historical_strategy, record_outcome


@dataclass
class ResponsePlan:
    strategy: str
    reason: str


APPROVED_STRATEGIES = [
    "AUDIO_DIRECTIONAL_A",
    "LIGHT_PLUS_AUDIO_B",
    "AUDIO_DIRECTIONAL_C",
    "FARMER_ESCALATION",
]


def select_strategy(db: Session, species: str, zone: str, risk_level: str) -> ResponsePlan:
    remembered = choose_historical_strategy(db, species, zone)
    if remembered in APPROVED_STRATEGIES:
        return ResponsePlan(remembered, "Selected from farm response memory")
    if risk_level == "HIGH":
        return ResponsePlan("AUDIO_DIRECTIONAL_A", "High-risk intrusion: approved first-line deterrence")
    return ResponsePlan("LIGHT_PLUS_AUDIO_B", "Moderate-risk intrusion: configurable non-harmful response")


def adaptive_retry(db: Session, species: str, zone: str, failed_strategy: str) -> ResponsePlan:
    next_strategy = {
        "AUDIO_DIRECTIONAL_A": "LIGHT_PLUS_AUDIO_B",
        "LIGHT_PLUS_AUDIO_B": "AUDIO_DIRECTIONAL_C",
        "AUDIO_DIRECTIONAL_C": "FARMER_ESCALATION",
    }.get(failed_strategy, "FARMER_ESCALATION")
    return ResponsePlan(next_strategy, "Initial strategy produced no verified retreat; adaptive retry selected")


def close_loop(db: Session, species: str, zone: str, strategy: str, outcome: str):
    success = outcome == "retreated"
    return record_outcome(db, species, zone, strategy, success, outcome)
