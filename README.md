# ACIT4420 Mandatory Assignment I - Option A: Smart Fitness Session Analyzer

Stephanie Norna Schraml
Student number: 421966

## Short description

This program analyzes fitness session data from sensors (heart rate, skin response, temperature, activity level). It checks if the readings make sense, calculates averages, and classifies the session as resting, moderate activity, high activity, recovering, or insufficient data. It uses the instructor's data generator to create realistic session data for a participant.

## Class design and responsibilities

- **Participant** - holds one person's baseline measurements (baseline heart rate, skin response, temperature). It doesn't do anything except store this data.
- **Observation** - holds one sensor reading from one point in time. It also keeps track of whether the reading is valid or not, and has methods to check and update this.
- **Session** - combines one Participant with a list of Observations. It also has a classmethod that builds a full Session directly from the data generator, so I don't have to manually convert the raw dictionaries myself every time.
- **Validator** - a base class for validation rules. It has one method, `check()`, that always returns True. This exists so HeartRateValidator and ActivityLevelValidator can override it with their own rules.
- **HeartRateValidator** and **ActivityLevelValidator** - inherit from Validator and override `check()` with rules for what counts as a realistic heart rate (35-205 bpm) and a realistic activity level (0-1).

## Where the OOP concepts are used

- **Composition**: Session is made up of one Participant and a list of Observation objects.
- **Encapsulation**: Observation keeps its validity status in `_is_valid`, which can only be changed through `mark_invalid()` and read through `is_valid()`. Nothing outside the class changes `_is_valid` directly.
- **Inheritance and overriding**: HeartRateValidator and ActivityLevelValidator both inherit from Validator and override the `check()` method with their own logic.
- **Classmethod**: `Session.from_generated_data()` is a classmethod that works as an alternative constructor, building a Session straight from the generator's output.
- **Standalone functions**: `average_heart_rate()`, `min_max_activity()`, `classify_session()`, and `format_report()` are all separate functions that take a session or a list of observations and return a result.

## Assumptions and classification rules

An observation is only used in the analysis if both its heart rate and activity level pass validation. If more than half of a session's observations are invalid, the session is classified as "insufficient data" instead of trying to analyze it.

For sessions with enough valid data, the classification is based on how far the average heart rate is from the participant's baseline:
- Less than 15 bpm above baseline: resting
- Less than 45 bpm above baseline: moderate activity
- 45 bpm or more above baseline: high activity

There's also a separate check for "recovering": if the first half of the session has a heart rate that is both much higher than baseline and clearly dropping compared to the second half, it's classified as recovering instead, even if the overall average would otherwise put it in a different category.

## How to install and run

1. Clone the repository:
   `git clone https://github.com/stephiens/acit4420_optionA.git`
2. Go into the folder:
   `cd acit4420_optionA`
3. Run the program (no external packages needed, only the Python standard library):
   `python3 main.py`
   
   On Windows, if `python3` is not recognized, use:
   `py main.py`
4. To run the tests:
   `python3 -m unittest tests.py -v`

## Example output

Running `python3 main.py` produces a report for each of the 5 scenarios, followed by all results as dictionaries:

Session Report for P001
Classification: resting
Baseline heart rate: 78 bpm
Average heart rate: 80.0 bpm
Activity level range: 0.04 to 0.18
Usable observations: 12 out of 12

Session Report for P001
Classification: moderate activity
Baseline heart rate: 78 bpm
Average heart rate: 105.8 bpm
Activity level range: 0.39 to 0.62
Usable observations: 12 out of 12

Session Report for P001
Classification: high activity
Baseline heart rate: 78 bpm
Average heart rate: 135.7 bpm
Activity level range: 0.69 to 0.91
Usable observations: 12 out of 12

Session Report for P001
Classification: recovering
Baseline heart rate: 78 bpm
Average heart rate: 112.8 bpm
Activity level range: 0.10 to 0.88
Usable observations: 12 out of 12

Session Report for P001
Classification: insufficient data
Baseline heart rate: 78 bpm
Average heart rate: 105.3 bpm
Activity level range: 0.10 to 0.74
Usable observations: 3 out of 12

## Known limitations

- The classification rules use fixed numbers (like 15 and 45 bpm) that I picked based on testing, not from any medical source. A different threshold could give different results for borderline cases.
- The program only tests using the built-in data generator's scenarios and a fixed set of sample data. It has not been tested against real sensor data.
- If a session has exactly 50% invalid observations, it is still analyzed instead of marked "insufficient data", since the check is for less than half being valid.