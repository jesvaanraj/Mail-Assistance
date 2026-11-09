
"""
Core logic: patient profile, red-flag check, Ollama AI analysis,
escalation, report generation, and saving.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

from prompts import ANALYSIS_PROMPT, DISCLAIMER, SYSTEM_PROMPT

# Load environment variables from .env
load_dotenv()

# Ollama configuration
MODEL = os.getenv("OPENAI_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = "http://localhost:11434/v1"

REPORTS_DIR = Path(__file__).parent / "reports"

RISK_ORDER = [
    "routine",
    "see_doctor_soon",
    "urgent",
    "emergency"
]

RISK_LABEL = {
    "routine": "Routine - self-care may be enough",
    "see_doctor_soon": "See a doctor soon",
    "urgent": "Urgent - seek care today",
    "emergency": "EMERGENCY - get help now",
}

# Rule-based safety net: independent of the AI model.
RED_FLAGS = [
    "chest pain",
    "chest tightness",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "trouble breathing",
    "shortness of breath",
    "severe bleeding",
    "heavy bleeding",
    "coughing blood",
    "vomiting blood",
    "unconscious",
    "fainted",
    "seizure",
    "stroke",
    "face drooping",
    "slurred speech",
    "sudden weakness",
    "sudden numbness",
    "worst headache",
    "confusion",
    "suicidal",
    "want to die",
    "kill myself",
    "overdose",
    "poisoning",
    "anaphylaxis",
    "throat swelling",
    "swollen tongue",
]

_client = None


# ---------- 1. Ollama Client ----------

def get_client() -> OpenAI:
    """
    Connect to the locally running Ollama server
    through its OpenAI-compatible API.
    """

    global _client

    if _client is None:
        _client = OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key="ollama"
        )

    return _client


# ---------- 2. Patient Profile ----------

def build_profile(data: Dict[str, Any]) -> Dict[str, str]:

    def clean(key: str, default: str = "Not provided") -> str:
        value = str(data.get(key, "") or "").strip()
        return value[:1000] if value else default

    profile = {
        "age": clean("age"),
        "sex": clean("sex"),
        "symptoms": clean("symptoms", ""),
        "duration": clean("duration"),
        "severity": clean("severity"),
        "conditions": clean("conditions", "None reported"),
        "medications": clean("medications", "None reported"),
        "allergies": clean("allergies", "None reported"),
    }

    if not profile["symptoms"]:
        raise ValueError("Please describe your symptoms.")

    if profile["age"] != "Not provided":
        if (
            not profile["age"].isdigit()
            or not (0 <= int(profile["age"]) <= 120)
        ):
            raise ValueError(
                "Age must be a number between 0 and 120."
            )

    return profile


# ---------- 3. Red-Flag Detection ----------

def detect_red_flags(profile: Dict[str, str]) -> List[str]:

    text = " ".join(profile.values()).lower()

    return [
        flag for flag in RED_FLAGS
        if flag in text
    ]


# ---------- 4. Ollama AI Analysis ----------

def _call_gpt(user_prompt: str) -> Dict[str, Any]:
    """
    Calls Llama 3.2 through Ollama.
    The function name is retained to avoid changing
    other parts of the existing application.
    """

    try:
        response = get_client().chat.completions.create(
            model=MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                },
            ],
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content

        if not raw:
            raise ValueError("The model returned an empty response.")

        raw = raw.strip()

        # Remove Markdown JSON code fences if present.
        raw = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            raw,
            flags=re.IGNORECASE
        ).strip()

        try:
            return json.loads(raw)

        except json.JSONDecodeError:
            # Attempt to extract a JSON object from the response.
            match = re.search(r"\{.*\}", raw, re.DOTALL)

            if match:
                return json.loads(match.group(0))

            raise ValueError(
                "The model did not return a valid JSON response. "
                "Please try again."
            )

    except Exception as error:
        print(f"Ollama API Error: {error}")
        raise


# ---------- 5. Full Analysis Pipeline ----------

def analyze_symptoms(data: Dict[str, Any]) -> Dict[str, Any]:

    # Build patient profile.
    profile = build_profile(data)

    # Check for emergency warning signs.
    flags = detect_red_flags(profile)

    # Prepare the AI prompt.
    prompt = ANALYSIS_PROMPT.format(**profile)

    # Get analysis from Ollama.
    result = _call_gpt(prompt)

    # Normalize model output.
    result.setdefault("reported_symptoms", [])
    result.setdefault("possible_conditions", [])
    result.setdefault("follow_up_questions", [])
    result.setdefault("self_care", [])

    risk = result.get("risk_level", "see_doctor_soon")

    if risk not in RISK_ORDER:
        risk = "see_doctor_soon"

    # Rule-based emergency escalation.
    if flags:
        risk = "emergency"

        result["risk_reason"] = (
            f"Warning signs mentioned: {', '.join(flags)}. "
            + str(result.get("risk_reason", ""))
        ).strip()

        result["medical_attention"] = (
            "Seek emergency medical care immediately. "
            + str(result.get("medical_attention", ""))
        ).strip()

    result["risk_level"] = risk
    result["risk_label"] = RISK_LABEL[risk]
    result["red_flags"] = flags
    result["disclaimer"] = DISCLAIMER
    result["profile"] = profile

    return result


# ---------- 6. Report Formatting ----------

def _bullets(items) -> str:

    if not items:
        return "• Not specified"

    if isinstance(items, str):
        items = [items]

    return "\n".join(
        f"• {item}" for item in items
    )


def format_report(r: Dict[str, Any]) -> str:

    p = r.get("profile", {})

    conditions = "\n".join(
        f"{n}. {c.get('name', '?')} "
        f"({c.get('likelihood', '')}) - "
        f"{c.get('reason', '')}"
        for n, c in enumerate(
            r.get("possible_conditions", []),
            1
        )
        if isinstance(c, dict)
    ) or "Not specified"

    return f"""
MEDICAL SYMPTOM ANALYSIS
--------------------------------

Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}

Patient Profile:

Age: {p.get('age', 'Not provided')}
Sex: {p.get('sex', 'Not provided')}
Severity: {p.get('severity', 'Not provided')}

Conditions: {p.get('conditions', 'Not provided')}
Medications: {p.get('medications', 'Not provided')}
Allergies: {p.get('allergies', 'Not provided')}

Reported Symptoms:

{_bullets(r.get('reported_symptoms'))}

Duration:

{p.get('duration', 'Not provided')}

Possible Conditions:

{conditions}

Why These Were Considered:

{r.get('why_considered', 'Not specified')}

Additional Information Needed:

{_bullets(r.get('follow_up_questions'))}

General Self-care:

{_bullets(r.get('self_care'))}

Risk Level:

{r.get('risk_label', 'Not specified')}

{r.get('risk_reason', '')}

Medical Attention:

{r.get('medical_attention', 'Not specified')}

Disclaimer:

{r.get('disclaimer', DISCLAIMER)}

--------------------------------
This report is AI-generated and is not a medical diagnosis.
"""


# ---------- 7. Save Report ----------

def save_report(result: Dict[str, Any]) -> str:

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    stem = datetime.now().strftime(
        "report_%Y%m%d_%H%M%S"
    )

    # Save JSON report.
    (REPORTS_DIR / f"{stem}.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Save TXT report.
    (REPORTS_DIR / f"{stem}.txt").write_text(
        format_report(result),
        encoding="utf-8"
    )

    return stem
