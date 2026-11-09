"""Prompt templates for the AI-Powered Medical Symptom Assistant."""

SYSTEM_PROMPT = (
    "You are a cautious medical information assistant. "
    "You help users understand symptoms and decide when to seek professional care. "
    "You NEVER give a definitive diagnosis; you list possible explanations and clearly "
    "communicate uncertainty. You do not recommend prescription drugs or specific doses. "
    "You always flag situations that need urgent or emergency care. "
    "Use ONLY the information the user provided; if something is missing, ask for it "
    "in the follow-up questions instead of assuming."
)

ANALYSIS_PROMPT = """Analyze the patient information below and return ONLY a valid JSON object
(no markdown, no commentary) with exactly these keys:

{{
  "reported_symptoms": ["string"],
  "duration": "string",
  "possible_conditions": [
    {{"name": "string", "likelihood": "more likely | possible | less likely", "reason": "string"}}
  ],
  "why_considered": "string (plain English, 2-3 sentences, express uncertainty)",
  "follow_up_questions": ["string"],
  "self_care": ["string (general, non-prescription self-care only)"],
  "risk_level": "routine | see_doctor_soon | urgent | emergency",
  "risk_reason": "string",
  "medical_attention": "string (when to seek professional evaluation)"
}}

Rules:
- Give 2-4 possible conditions, ordered from most to least likely. Never present one as confirmed.
- Say that the symptoms alone are not sufficient for a diagnosis.
- follow_up_questions: 3-5 questions that would help narrow things down (e.g. exact temperature,
  breathing difficulty, associated symptoms).
- risk_level: choose "emergency" for signs such as chest pain, severe breathing difficulty,
  stroke signs, heavy bleeding, confusion, or suicidal thoughts. Choose the higher level when unsure.
- Take age, sex, existing conditions, medications and allergies into account where relevant.
- Do not invent symptoms or facts that were not provided.

PATIENT INFORMATION:
Age: {age}
Sex: {sex}
Symptoms (user's own words): {symptoms}
Duration: {duration}
Severity: {severity}
Existing medical conditions: {conditions}
Current medications: {medications}
Allergies: {allergies}
"""

DISCLAIMER = (
    "This is an informational AI analysis and not a medical diagnosis. "
    "It cannot replace a doctor. If you think you are having a medical emergency, "
    "contact your local emergency number immediately (112 in India)."
)
