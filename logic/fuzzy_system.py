"""Fuzzy Inference System (Mamdani) untuk skor urgensi/relevansi."""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Input
duration = ctrl.Antecedent(np.arange(0, 61, 1), "duration_months")     # 0-60 bulan
settings = ctrl.Antecedent(np.arange(0, 6, 1), "settings_count")        # 0-5 setting
match_ratio = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "match_ratio")   # 0-1
red_flags = ctrl.Antecedent(np.arange(0, 4, 1), "red_flag_count")       # 0-3

# Output
urgency = ctrl.Consequent(np.arange(0, 101, 1), "urgency_score")        # 0-100

# Membership functions
duration["singkat"] = fuzz.trimf(duration.universe, [0, 0, 6])
duration["sedang"] = fuzz.trimf(duration.universe, [3, 12, 24])
duration["lama"] = fuzz.trimf(duration.universe, [12, 60, 60])

settings["sedikit"] = fuzz.trimf(settings.universe, [0, 0, 2])
settings["sedang"] = fuzz.trimf(settings.universe, [1, 3, 4])
settings["banyak"] = fuzz.trimf(settings.universe, [3, 5, 5])

match_ratio["rendah"] = fuzz.trimf(match_ratio.universe, [0, 0, 0.5])
match_ratio["tinggi"] = fuzz.trimf(match_ratio.universe, [0.4, 1, 1])

red_flags["tidak_ada"] = fuzz.trimf(red_flags.universe, [0, 0, 1])
red_flags["ada"] = fuzz.trimf(red_flags.universe, [1, 3, 3])

urgency["rendah"] = fuzz.trimf(urgency.universe, [0, 0, 40])
urgency["sedang"] = fuzz.trimf(urgency.universe, [30, 50, 70])
urgency["tinggi"] = fuzz.trimf(urgency.universe, [60, 100, 100])

# Rules
rules = [
    ctrl.Rule(red_flags["ada"], urgency["tinggi"]),
    ctrl.Rule(duration["lama"] & settings["banyak"] & match_ratio["tinggi"], urgency["tinggi"]),
    ctrl.Rule(duration["lama"] & match_ratio["tinggi"], urgency["sedang"]),
    ctrl.Rule(duration["sedang"] & settings["sedang"], urgency["sedang"]),
    ctrl.Rule(duration["singkat"] & match_ratio["rendah"], urgency["rendah"]),
    ctrl.Rule(match_ratio["rendah"] & red_flags["tidak_ada"], urgency["rendah"]),
    ctrl.Rule(duration["lama"] & match_ratio["rendah"], urgency["sedang"]),
]

urgency_ctrl = ctrl.ControlSystem(rules)


def compute_urgency(duration_months, settings_count, match_ratio_val, red_flag_count):
    """
    Hitung skor urgensi 0-100.
    """
    sim = ctrl.ControlSystemSimulation(urgency_ctrl)
    sim.input["duration_months"] = min(max(duration_months, 0), 60)
    sim.input["settings_count"] = min(max(settings_count, 0), 5)
    sim.input["match_ratio"] = min(max(match_ratio_val, 0), 1)
    sim.input["red_flag_count"] = min(max(red_flag_count, 0), 3)
    try:
        sim.compute()
        return float(sim.output["urgency_score"])
    except Exception:
        return 50.0  # default kalau fuzzy gagal