# Experiment 6: AI-Powered Medical Symptom Assistant using GPT-4
**Course:** 24CS2506 – Building Applications using GPT-4

A web app where the user enters their age, sex and symptoms in natural language. GPT-4 returns a structured analysis (possible conditions, follow-up questions, self-care, risk level) with a disclaimer. Reports are saved automatically and can be downloaded.

> This is an educational project. It does **not** give a diagnosis and is not a substitute for a doctor.

## Workflow

```
User Input (web form) -> Patient Profile -> Symptom Extraction -> Context Analysis
 -> Prompt Generation -> GPT-4 -> Symptoms / Possible Conditions / Follow-up Questions
 -> Risk / Escalation Assessment -> Structured Response -> Disclaimer -> Save Report
```

## Project structure

```
medical_assistant/
├── app.py               # Flask server (routes: / and /api/analyze)
├── assistant.py         # profile, red-flag check, GPT-4 call, escalation, report, saving
├── prompts.py           # system prompt, analysis prompt, disclaimer
├── templates/index.html # frontend page
├── static/style.css     # frontend styling
├── static/app.js        # frontend logic (calls /api/analyze)
├── requirements.txt
├── .env.example         # copy to .env and add your key
└── reports/             # saved reports (created automatically)
```

## Setup in VS Code

1. Open this folder in VS Code (`File > Open Folder`).
2. Open the terminal and create a virtual environment:

   **Windows**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   **macOS / Linux**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. `Ctrl+Shift+P` -> **Python: Select Interpreter** -> pick the `venv` one.
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` from the template and add your OpenAI key:
   ```
   copy .env.example .env      (Windows)
   cp .env.example .env        (macOS / Linux)
   ```

## Run

```
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

Try: *"I've had a fever and cough since yesterday. I also feel tired and have a mild headache."* (Age 22, Mild, 2 days). Then try *"chest pain and difficulty breathing"* to see the emergency escalation.

## Safety design

- The system prompt forbids definitive diagnoses and prescription/dose advice.
- Possible conditions are ranked with likelihood and a reason, and uncertainty is stated.
- **Red-flag check in code** (`RED_FLAGS` in `assistant.py`): words like "chest pain" or "difficulty breathing" force the risk level to *emergency* even if the model under-rates it.
- The disclaimer is added by code, not by the model, so it is always present.
- The frontend writes model output with `textContent`, so it cannot inject HTML.

## Troubleshooting

- `OPENAI_API_KEY not found` -> make sure `.env` (not `.env.example`) exists in this folder.
- `ModuleNotFoundError` -> activate the venv and run `pip install -r requirements.txt`.
- Model access error -> set `OPENAI_MODEL=gpt-4o` in `.env`.
