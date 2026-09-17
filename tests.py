import unittest
from main import Observation, average_heart_rate, min_max_activity
from sample_data import SAMPLE_OBSERVATIONS


def build_sample_observations():
    """Convert raw sample_data dictionaries into real and validated Observation objects."""
    observations = []
    for data in SAMPLE_OBSERVATIONS:
        observation = Observation(
            timestamp=data["timestamp"],
            heart_rate=data["heart_rate"],
            skin_response=data["skin_response"],
            temperature=data["temperature"],
            activity_level=data["activity_level"],
            signal_quality=data["signal_quality"],
        )
        observation.validate()
        observations.append(observation)
    return observations


class TestValidation(unittest.TestCase):
    """Tests that Observation.validate() correctly marks good and bad sample data."""

    def test_valid_observations_are_marked_valid(self):
        """Check that observations with realistic values stay marked as valid."""
        observations = build_sample_observations()
        self.assertTrue(observations[0].is_valid())
        self.assertTrue(observations[1].is_valid())
        self.assertTrue(observations[5].is_valid())

    def test_invalid_observations_are_marked_invalid(self):
        """Check that observations with missing or impossible values get marked invalid."""
        observations = build_sample_observations()
        self.assertFalse(observations[2].is_valid())
        self.assertFalse(observations[3].is_valid())
        self.assertFalse(observations[4].is_valid())


class TestAnalysisFunctions(unittest.TestCase):
    """Tests that the analysis functions calculate correct results from known sample data."""

    def test_average_heart_rate_uses_only_valid_observations(self):
        """Check that average_heart_rate matches the hand-calculated expected value."""
        observations = build_sample_observations()
        expected_average = (72 + 75 + 76) / 3
        self.assertAlmostEqual(average_heart_rate(observations), expected_average)

    def test_min_max_activity_uses_only_valid_observations(self):
        """Check that min_max_activity returns the correct known minimum and maximum."""
        observations = build_sample_observations()
        min_activity, max_activity = min_max_activity(observations)
        self.assertAlmostEqual(min_activity, 0.10)
        self.assertAlmostEqual(max_activity, 0.18)

# Run all tests when this file is executed directly
if __name__ == "__main__":
    unittest.main()