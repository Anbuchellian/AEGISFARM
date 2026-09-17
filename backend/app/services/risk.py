from dataclasses import dataclass


@dataclass
class RiskAssessment:
    score: float
    level: str
    reasons: list[str]


def assess_risk(confidence: float, zone: str, direction: str, historical_frequency: int = 0) -> RiskAssessment:
    score = 0.0
    reasons: list[str] = []

    score += min(max(confidence, 0), 1) * 30
    if confidence > 0.75:
        reasons.append("High detection confidence")

    if direction.lower() in {"south-east", "east", "south", "approaching crop"}:
        score += 20
        reasons.append("Movement is oriented toward protected crop area")

    if zone.lower() in {"north-west", "zone 3", "entry point"}:
        score += 20
        reasons.append("Zone has elevated boundary risk")

    score += min(historical_frequency, 5) * 6
    if historical_frequency:
        reasons.append("Historical intrusion activity detected in this context")

    score += 10
    level = "LOW" if score < 35 else "MEDIUM" if score < 65 else "HIGH"
    return RiskAssessment(round(min(score, 100), 1), level, reasons)
