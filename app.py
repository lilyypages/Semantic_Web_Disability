"""Flask app: jembatan antara UI Kindred Care dan ontology reasoning."""

from flask import Flask, render_template, request, jsonify
from logic.mapping import (
    AREA_TO_SIGN_CODES, RED_FLAG_SIGNS, RED_FLAG_QUESTIONS,
    DURATION_TO_MONTHS, SETTING_KEYS, SIGN_LABELS,
)
from logic.reasoner import analyze_case
from logic.fuzzy_system import compute_urgency

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/signs")
def api_signs():
    """Kirim daftar area + sign untuk di-render di basics.html."""
    areas = [
        {"key": k, "label": k.replace("_", " ").title(), "signs": [
            {"code": c, "label": SIGN_LABELS.get(c, c)} for c in codes
        ]}
        for k, codes in AREA_TO_SIGN_CODES.items()
    ]
    return jsonify({
        "areas": areas,
        "red_flags": [
            {**q, "label_short": SIGN_LABELS.get(q["code"], q["label"])}
            for q in RED_FLAG_QUESTIONS
        ],
    })


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """
    Terima JSON:
    {
      "age_months": 36,
      "area": "communication",
      "observed_signs": ["K1", "K3", "S1"],
      "duration": "several_months",
      "settings": ["home", "school"],
      "red_flags": ["K6"]
    }
    """
    data = request.get_json(force=True) or {}

    age_months = int(data.get("age_months", 24))
    observed = list(data.get("observed_signs", []))
    duration_key = data.get("duration", "several_months")
    duration_months = DURATION_TO_MONTHS.get(duration_key, 3)
    settings = list(data.get("settings", []))
    settings_count = len([s for s in settings if s in SETTING_KEYS]) or 1
    red_flags = list(data.get("red_flags", []))

    # Gabungkan sign utama + red flag yang dipilih
    all_signs = list(dict.fromkeys(observed + red_flags))

    # Reasoning
    result = analyze_case(
        sign_codes=all_signs,
        age_months=age_months,
        duration_months=duration_months,
        settings_count=settings_count,
    )

    # Fuzzy scoring per kondisi
    for cond in result["related_conditions"]:
        cond["urgency_score"] = round(compute_urgency(
            duration_months=duration_months,
            settings_count=settings_count,
            match_ratio_val=cond["ratio"],
            red_flag_count=len(red_flags),
        ), 1)

    # Urgensi keseluruhan (ambil max)
    overall = max(
        [c["urgency_score"] for c in result["related_conditions"]] or [0]
    ) if result["related_conditions"] else 0
    if red_flags:
        overall = max(overall, 90)

    result["overall_urgency"] = round(overall, 1)
    result["red_flags_selected"] = red_flags
    result["is_red_flag_case"] = "RedFlagCase" in result["inferred_classes"]

    return jsonify(result)


@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/basics")
def basics():
    return render_template("basics.html")


@app.route("/questions")
def questions():
    return render_template("questions.html")


@app.route("/results")
def results():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)