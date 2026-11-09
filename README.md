# Experiment 6: AI-Powered Medical Symptom Assistant using Ollama and Llama 3.2

**Course:** 24CS2506 – Building Applications using GPT-4

An AI-powered web application that allows users to enter their age, sex, and symptoms in natural language. The application uses **Llama 3.2 (3B) through Ollama** to generate structured health information, including possible conditions, follow-up questions, general self-care suggestions, and risk-level assessment.

The application also includes a rule-based red-flag detection system to identify potentially serious symptoms and automatically escalate the risk level. Reports are saved in JSON and TXT formats.

> **Disclaimer:** This is an educational project. It does not provide a medical diagnosis and is not a substitute for professional medical advice.

## Features

- **Patient Information:** Collects age, sex, symptoms, duration, severity, existing medical conditions, medications, and allergies.
- **AI-Powered Symptom Analysis:** Uses Llama 3.2 to analyze user-provided symptoms.
- **Possible Conditions:** Provides possible explanations with likelihood and reasoning.
- **Follow-up Questions:** Generates additional questions to understand the patient's symptoms.
- **Self-Care Suggestions:** Provides general health and wellness information.
- **Risk Assessment:** Categorizes risk into routine, see a doctor soon, urgent, and emergency.
- **Red-Flag Detection:** Uses rule-based checks to identify potentially serious warning signs.
- **Automatic Report Generation:** Saves analysis reports in JSON and TXT formats.
- **Local AI Processing:** Runs the language model locally through Ollama without requiring paid OpenAI API calls.

## Workflow

```text
User Input (Web Form)
        |
        v
Patient Profile Creation
        |
        v
Symptom Extraction
        |
        v
Context Analysis
        |
        v
Prompt Generation
        |
        v
Ollama API
        |
        v
Llama 3.2 (3B)
        |
        v
Structured AI Response
        |
        v
Red-Flag Detection
        |
        v
Risk / Escalation Assessment
        |
        v
Disclaimer Addition
        |
        v
Report Generation
        |
        v
Save Report (JSON + TXT)
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Ollama | Local LLM runtime |
| Llama 3.2 (3B) | AI-powered symptom analysis |
| OpenAI Python SDK | Communicates with Ollama through its OpenAI-compatible API |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions and API requests |
| JSON | Structured AI responses and report storage |
| Python-dotenv | Environment variable management |

## Project Structure

```text
medical_assistant/
│
├── app.py                  # Flask server and API routes
├── assistant.py            # Patient profile, AI analysis, red-flag detection,
│                           # risk assessment, report generation and saving
├── prompts.py              # System prompt, analysis prompt and disclaimer
│
├── templates/
│   └── index.html          # Frontend page
│
├── static/
│   ├── style.css           # Frontend styling
│   └── app.js              # Frontend logic and API requests
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Files excluded from Git
│
└── reports/                # Generated reports (created automatically)
```

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or later
- Visual Studio Code
- Git
- Ollama

### 1. Clone the Repository

```bash
git clone https://github.com/jesvaanraj/medical_assistant.git
```

Navigate into the project folder:

```bash
cd medical_assistant
```

### 2. Install Ollama

Download and install Ollama from:

https://ollama.com/

### 3. Download Llama 3.2

Open the terminal and execute:

```bash
ollama pull llama3.2:3b
```

Verify that the model is installed:

```bash
ollama list
```

### 4. Create a Python Virtual Environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Select Python Interpreter in VS Code

1. Press `Ctrl + Shift + P`.
2. Search for `Python: Select Interpreter`.
3. Select the Python interpreter inside the `venv` folder.

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Configure Environment Variables

Create a `.env` file from `.env.example`.

**Windows:**

```powershell
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Add the following configuration to `.env`:

```env
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3.2:3b
```

**Note:** The API key value `ollama` is a placeholder used by the OpenAI-compatible Python client. No paid OpenAI API key is required. The application connects to Ollama at `http://localhost:11434/v1`.

## Running the Application

### 1. Start Ollama

Make sure the Ollama service is running.

You can test the model using:

```bash
ollama run llama3.2:3b
```

### 2. Start the Flask Application

Activate your virtual environment and execute:

```bash
python app.py
```

### 3. Open the Application

Visit the following address in your browser:

```text
http://127.0.0.1:5000
```

The Medical Symptom Assistant interface should now be available.

## Sample Input

Try the following example to test the application:

| Field | Input |
|---|---|
| Age | 21 |
| Sex | Male |
| Severity | Mild |
| Symptoms | Fever, cough, tiredness and mild headache |
| Duration | 2 days |
| Existing Medical Conditions | None |
| Current Medications | None |
| Allergies | None |

Click **Analyze Symptoms** to generate the AI-powered response.

## Safety Design

The application includes multiple safety mechanisms:

- **System Prompt Restrictions:** Instructs the AI model not to provide definitive diagnoses or prescription and dosage advice.
- **Possible Conditions:** Presents possible explanations with likelihood and reasoning, while communicating uncertainty.
- **Rule-Based Red-Flag Detection:** The `RED_FLAGS` list in `assistant.py` checks for warning signs such as chest pain, difficulty breathing, severe bleeding, and other potentially serious symptoms.
- **Emergency Escalation:** Detected red flags automatically force the risk level to emergency.
- **Code-Based Disclaimer:** The medical disclaimer is added by the application rather than relying on the AI model to generate it.
- **Safe Frontend Rendering:** The frontend uses `textContent` to display model output instead of inserting it as HTML.

**Important:** Red-flag detection is a basic keyword-based safety mechanism. It cannot identify every emergency or replace professional medical assessment.

## Troubleshooting

### Ollama connection error

Make sure Ollama is running and try:

```bash
ollama list
```

If the model is missing:

```bash
ollama pull llama3.2:3b
```

### ModuleNotFoundError

Activate the virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

### Model not found

Check the installed models:

```bash
ollama list
```

Make sure `.env` contains:

```env
OPENAI_MODEL=llama3.2:3b
```

### Application cannot connect to Ollama

Verify that the Ollama service is available at:

```text
http://localhost:11434
```

The application uses the OpenAI-compatible endpoint:

```text
http://localhost:11434/v1
```

### Port 5000 already in use

Stop the other Flask application using port 5000 or configure a different port in `app.py`.

## Future Enhancements

- Support for additional locally hosted language models.
- PDF report export.
- Improved symptom extraction and medical terminology recognition.
- Enhanced emergency symptom detection.
- Conversation history and patient session management.
- Improved response validation and structured output handling.

## Author

**J F JESVAAN RAJ**

Computer Science and Engineering Student

GitHub: https://github.com/jesvaanraj

---

**Built as part of Experiment 6 – AI-Powered Medical Symptom Assistant.**

*Powered by Python, Flask, Ollama and Llama 3.2.*
