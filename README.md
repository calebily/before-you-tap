# Before You Tap

An AI safety companion that helps older adults analyse suspicious images and audio messages before they act.

> Status: image selection, preview, and secure upload validation are working. Gemini risk
> analysis and audio upload are the next development stages.

## MVP

Before You Tap accepts user-selected:

- images of suspicious messages, emails, chats, or letters; and
- existing audio files such as voicemails and voice messages.

The agent will return a plain-language risk assessment, the warning signs it found, uncertainty, and safe next steps. It does not monitor live calls or activate a microphone in the background.

Read the approved [MVP specification](docs/MVP_SPEC.md).

## Stack

- Python 3.12
- FastAPI
- Google Agent Development Kit (ADK)
- Gemini 3.5 Flash through Vertex AI
- Cloud Run

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8080
```

Open <http://localhost:8080>. Health check: <http://localhost:8080/healthz>.

The default configuration does not call an AI service. For local development, the app is ready
to use the Gemini API free tier through Google AI Studio after `GOOGLE_API_KEY` is added to the
local `.env`. Never commit that file or share the key. For the final Google Cloud deployment, set
`GOOGLE_GENAI_USE_VERTEXAI=true` and provide `GOOGLE_CLOUD_PROJECT` instead.

Run tests:

```bash
pytest
```

## Privacy and security

- Do not commit credentials, real private messages, or real voicemail files.
- Demo and test assets must be fictional and non-sensitive.
- Uploaded content will be processed only for the current analysis and will not be intentionally retained in the MVP.
- Uploaded files are currently read only for validation and immediately discarded.
- The UI must clearly disclose cloud-AI processing before a user uploads a file.

## Repository layout

```text
app/                 FastAPI application and accessible web UI
app/services/        Input validation and analysis services
docs/                Product and architecture documentation
tests/               Automated tests
```

## Development disclosure

OpenAI Codex is used as an AI coding assistant. Product direction, implementation decisions, review, testing, and the final submission remain the entrant's responsibility.
