from data_generator import generate_fitness_data, available_scenarios


class Participant:
    """Represents one person taking part in a fitness session, along with their baseline measurements."""

    def __init__(self, participant_id, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.participant_id = participant_id
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

class Observation:
    """Represents one single sensor reading taken at a specific point in time during a session."""

    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality
        self._is_valid = True

    def mark_invalid(self):
        """Flip this observation's validity flag to False (called when a check fails)."""
        self._is_valid = False

    def is_valid(self):
        """Return whether this observation is currently considered valid."""
        return self._is_valid

class Session:
    """Groups one Participant together with a list of Observation objects for a single workout session."""

    def __init__(self, participant, observations):
        self.participant = participant
        self.observations = observations

    @classmethod
    def from_generated_data(cls, participant_id, scenario, seed=None, number_of_windows=12):
        """Build a Session directly from the instructor's data generator, converting raw dictionaries into real Participant and Observation objects."""
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
            observation_list.append(Observation(
                timestamp=observation["timestamp"],
                heart_rate=observation["heart_rate"],
                skin_response=observation["skin_response"],
                temperature=observation["temperature"],
                activity_level=observation["activity_level"],
                signal_quality=observation["signal_quality"],
            ))

        return cls(participant, observation_list)

class Validator:
    """Base class for a validation rule. Subclasses override check() with their own logic."""

    def check(self, value):
        """Return True if value passes this rule. The base version accepts everything; subclasses override this."""
        return True

class HeartRateValidator(Validator):
    """Validates that a heart rate reading falls within a physically realistic range for a human."""

    def check(self, value):
        """Return True if the heart rate is a real number within a realistic human range."""
        if value is None:
            return False
        return 35 <= value <=205

class ActivityLevelValidator(Validator):
    """Validates that an activity level reading falls within the expected 0-1 range."""

    def check(self, value):
        """Return True if the activity level is a real number between 0 and 1."""
        if value is None:
            return False
        return 0 <= value <=1
    