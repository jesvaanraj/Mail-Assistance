"""Flask server for the AI-Powered Medical Symptom Assistant (Experiment 6, 24CS2506).

Run:  python app.py   then open http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template, request

from assistant import analyze_symptoms, format_report, save_report

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    try:
        result = analyze_symptoms(data)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except RuntimeError as e:
        return jsonify(error=str(e)), 500
    except Exception as e:  # network / API errors
        return jsonify(error=f"Could not complete the analysis: {e}"), 502

    result["report_id"] = save_report(result)
    result["report_text"] = format_report(result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
