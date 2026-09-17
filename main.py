from data_generator import generate_fitness_data, available_scenarios


class Participant:
    """Represents one person taking part in a fitness session and their baseline measurements."""

    def __init__(self, participant_id, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.participant_id = participant_id
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

class Observation:
    """Represents one sensor reading taken at a specific point in time during a session."""

    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality
        self._is_valid = True

    def mark_invalid(self):
        """Flip observation's validity flag to False (called when check fails)."""
        self._is_valid = False

    def is_valid(self):
        """Return whether observation is currently considered valid."""
        return self._is_valid

    def validate(self):
        """Check observation's heart_rate and activity_level, marking it invalid if either fails."""
        heart_rate_validator = HeartRateValidator()
        activity_validator = ActivityLevelValidator()

        if not heart_rate_validator.check(self.heart_rate):
            self.mark_invalid()

        if not activity_validator.check(self.activity_level):
            self.mark_invalid()

class Session:
    """Groups Participant together with a list of Observation objects for a single workout session."""

    def __init__(self, participant, observations):
        self.participant = participant
        self.observations = observations

    @classmethod
    def from_generated_data(cls, participant_id, scenario, seed=None, number_of_windows=12):
        """Build Session directly from the instructor's data generator, converting raw dictionaries into real Participant and Observation objects."""
        profile, observations = generate_fitness_data(
            participant_id=participant_id,
            scenario=scenario,
            seed=seed,
            number_of_windows=number_of_windows,
        )

        participant = Participant(
            participant_id=profile["participant_id"],
            baseline_heart_rate=profile["baseline_heart_rate"],
            baseline_skin_response=profile["baseline_skin_response"],
            baseline_temperature=profile["baseline_temperature"],
        )

        observation_list = []
        for observation in observations:
            new_observation = Observation(
                timestamp=observation["timestamp"],
                heart_rate=observation["heart_rate"],
                skin_response=observation["skin_response"],
                temperature=observation["temperature"],
                activity_level=observation["activity_level"],
                signal_quality=observation["signal_quality"],
            )
            new_observation.validate()
            observation_list.append(new_observation)

        return cls(participant, observation_list)

class Validator:
    """Base class for validation rule. Subclasses override check() with their own logic."""

    def check(self, value):
        """Return True if value passes this rule. The base version accepts everything; subclasses override this."""
        return True

class HeartRateValidator(Validator):
    """Validates that heart rate readings falls within a physically realistic range for humans."""

    def check(self, value):
        """Return True if heart rate is a real number within a realistic human range."""
        if value is None:
            return False
        return 35 <= value <=205

class ActivityLevelValidator(Validator):
    """Validates that activity level reading falls within the expected 0-1 range."""

    def check(self, value):
        """Return True if the activity level is a real number between 0 and 1."""
        if value is None:
            return False
        return 0 <= value <=1


def average_heart_rate(observations):
    """Calculate the average heart rate across all valid observations in the list."""
    valid_heart_rates = [observation.heart_rate for observation in observations if observation.is_valid()]
    if not valid_heart_rates:
        return None
    return sum(valid_heart_rates) / len(valid_heart_rates)


def min_max_activity(observations):
    """Find the lowest and highest activity level among all valid observations."""
    valid_activity_levels = [observation.activity_level for observation in observations if observation.is_valid()]
    if not valid_activity_levels:
        return None, None
    return min(valid_activity_levels), max(valid_activity_levels)


def classify_session(session):
    """Determine whether a session was resting, moderate activity, high activity, recovering or had insufficient data."""
    total_count = len(session.observations)
    valid_observations = [observation for observation in session.observations if observation.is_valid()]
    valid_count = len(valid_observations)

    if valid_count < total_count / 2:
        return "insufficient data"

    midpoint = len(valid_observations) // 2
    first_half = valid_observations[:midpoint]
    second_half = valid_observations[midpoint:]

    first_half_average = average_heart_rate(first_half)
    second_half_average = average_heart_rate(second_half)

    baseline = session.participant.baseline_heart_rate
    overall_average = average_heart_rate(valid_observations)
    offset = overall_average - baseline

    if first_half_average is not None and second_half_average is not None:
        if first_half_average - second_half_average > 15 and first_half_average - baseline > 20:
            return "recovering"

    if offset < 15:
        return "resting"
    elif offset < 45:
        return "moderate activity"
    else:
        return "high activity"


def format_report(session, classification):
    """Build readable, multi-line console report describing this session."""
    total_count = len(session.observations)
    valid_count = len([observation for observation in session.observations if observation.is_valid()])

    average_hr = average_heart_rate(session.observations)
    min_activity, max_activity = min_max_activity(session.observations)

    lines = []
    lines.append(f"Session Report for {session.participant.participant_id}")
    lines.append(f"Classification: {classification}")
    lines.append(f"Baseline heart rate: {session.participant.baseline_heart_rate} bpm")

    if average_hr is not None:
        lines.append(f"Average heart rate: {average_hr:.1f} bpm")
    else:
        lines.append("Average heart rate: not available (no valid readings)")

    if min_activity is not None:
        lines.append(f"Activity level range: {min_activity:.2f} to {max_activity:.2f}")
    else:
        lines.append("Activity level range: not available (no valid readings)")

    lines.append(f"Usable observations: {valid_count} out of {total_count}")

    return "\n".join(lines)


if __name__ == "__main__":
    scenarios_to_run = ["resting", "moderate_activity", "high_activity", "recovery", "poor_quality"]
    all_results = []

    for scenario in scenarios_to_run:
        session = Session.from_generated_data(participant_id="P001", scenario=scenario, seed=42, number_of_windows=12)
        classification = classify_session(session)
        print(format_report(session, classification))
        print()

        total_count = len(session.observations)
        valid_count = len([observation for observation in session.observations if observation.is_valid()])
        average_hr = average_heart_rate(session.observations)
        min_activity, max_activity = min_max_activity(session.observations)

        result = {
            "participant_id": session.participant.participant_id,
            "scenario": scenario,
            "classification": classification,
            "average_heart_rate": average_hr,
            "min_activity": min_activity,
            "max_activity": max_activity,
            "valid_observations": valid_count,
            "total_observations": total_count,
        }
        all_results.append(result)

    print("All results as dictionaries:")
    for result in all_results:
        print(result)