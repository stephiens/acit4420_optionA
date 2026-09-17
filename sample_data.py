"""Fixed example data used for testing the analysis functions without relying on randomly generated data."""

SAMPLE_PROFILE = {
    "participant_id": "TEST001",
    "baseline_heart_rate": 70,
    "baseline_skin_response": 1.5,
    "baseline_temperature": 32.0,
}

SAMPLE_OBSERVATIONS = [
    {"timestamp": 0, "heart_rate": 72, "skin_response": 1.4, "temperature": 32.1, "activity_level": 0.10, "signal_quality": 0.95},
    {"timestamp": 1, "heart_rate": 75, "skin_response": 1.5, "temperature": 32.2, "activity_level": 0.15, "signal_quality": 0.93},
    {"timestamp": 2, "heart_rate": None, "skin_response": 1.5, "temperature": 32.2, "activity_level": 0.12, "signal_quality": 0.40},
    {"timestamp": 3, "heart_rate": 280, "skin_response": 1.6, "temperature": 32.3, "activity_level": 0.20, "signal_quality": 0.50},
    {"timestamp": 4, "heart_rate": 74, "skin_response": 1.5, "temperature": 32.1, "activity_level": -0.30, "signal_quality": 0.90},
    {"timestamp": 5, "heart_rate": 76, "skin_response": 1.5, "temperature": 32.2, "activity_level": 0.18, "signal_quality": 0.92},
]
