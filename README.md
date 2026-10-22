# ShipReady AI

**Check your hackathon submission readiness before the deadline.**

ShipReady AI is a Streamlit web app that helps hackathon participants organize submission requirements, identify missing items, track readiness, and download a readiness report.

## Features

- Track project submission requirements.
- View a readiness score based on completed requirements.
- Identify requirements that still need attention.
- Record evidence links and notes.
- Mark requirements as independently reviewed.
- Download a submission-readiness report.

## Live Demo

https://shipready-ai.streamlit.app/

## Run Locally

### Requirements

- Python
- pip

### Setup

```bash
git clone https://github.com/revanth2444-cmyk/shipready-ai.git
cd shipready-ai
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and launch the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important Limitations

Readiness is based on the information entered by the user. Evidence links are not automatically verified, and the report should not be treated as proof that a submission satisfies every event rule.

## Built For

No Hands: The Wispr Challenge — Track 1: Builders.

Wispr Flow is being used as part of the development workflow.

## Technology

- Python
- Streamlit
- GitHub
- Streamlit Community Cloud
