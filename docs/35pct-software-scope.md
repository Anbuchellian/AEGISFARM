# 35% Software Scope — AEGISFARM

## Demonstrable loop

1. Sensor/event input
2. AI detection
3. Species identification
4. Zone assignment
5. Risk assessment
6. Adaptive response strategy
7. Intervention record
8. Observation / retreat verification
9. Response memory update
10. Farmer dashboard

## Demo scenarios

### Scenario A — normal response
- Simulate wild boar in North-West
- AEGISFARM selects a permitted first-line strategy
- Retreat is verified
- Successful outcome is stored

### Scenario B — no response
- Simulate the same intrusion with `simulate_no_response=true`
- First response is recorded as `no_response`
- Adaptive retry selects a second permitted strategy
- Retreat is then verified
- Both outcomes are stored in response memory

## What is not claimed

- No field accuracy percentage is pre-filled.
- No wildlife deterrence success rate is pre-filled.
- Demo events are simulations until replaced by real sensor/camera events.
- User validation records must be populated from real testers.
