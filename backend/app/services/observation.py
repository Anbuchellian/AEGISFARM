from dataclasses import dataclass


@dataclass
class ObservationResult:
    outcome: str
    confidence: float
    next_state: str


def verify_retreat(simulate_no_response: bool = False) -> ObservationResult:
    if simulate_no_response:
        return ObservationResult("no_response", 0.92, "ADAPTIVE_RETRY")
    return ObservationResult("retreated", 0.90, "PROTECTION_CONFIRMED")
