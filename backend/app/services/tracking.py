from dataclasses import dataclass
from math import hypot


@dataclass
class TrackState:
    track_id: int
    x: float
    y: float
    vx: float
    vy: float


class SimpleTracker:
    """Lightweight trajectory estimator for prototype demos.
    Replace with ByteTrack/Ultralytics tracking during camera integration.
    """

    def __init__(self):
        self._next_id = 1
        self.tracks: dict[int, TrackState] = {}

    def update(self, x: float, y: float) -> TrackState:
        if not self.tracks:
            state = TrackState(self._next_id, x, y, 0.0, 0.0)
            self.tracks[state.track_id] = state
            self._next_id += 1
            return state
        state = next(iter(self.tracks.values()))
        vx, vy = x - state.x, y - state.y
        state.x, state.y, state.vx, state.vy = x, y, vx, vy
        return state

    @staticmethod
    def direction(state: TrackState) -> str:
        if hypot(state.vx, state.vy) < 0.01:
            return "Stationary"
        if abs(state.vx) > abs(state.vy):
            return "East" if state.vx > 0 else "West"
        return "South" if state.vy > 0 else "North"
