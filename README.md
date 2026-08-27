# Before You Tap

An AI safety companion that helps older adults analyse suspicious images and audio messages before they act.

> Status: multi-image and saved-audio selection, secure upload validation, Gemini risk analysis,
> and an accessible results view are working.

## MVP

Before You Tap accepts user-selected:

- up to five ordered images of one suspicious message, email, chat, or letter; and
- existing audio files such as voicemails and voice messages.

The agent considers all selected pages together and returns a plain-language risk assessment, the
warning signs it found, uncertainty, and safe next steps. Image uploads are limited to five files
and 20 MB in total; they can be selected, dragged into the page, or pasted from the clipboard.
The UI asks users to keep unrelated emails or conversations in separate checks. If unrelated
items are supplied accidentally, the model is instructed not to combine them into one narrative.
Audio checks accept one MP3, M4A, WAV, OGG, or WebM file up to 20 MB. It does not monitor live
calls or activate a microphone in the background.

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

The default configuration does not call an AI service. The recommended local setup uses Vertex AI
with Application Default Credentials (ADC): set `GOOGLE_GENAI_USE_VERTEXAI=true` and add your
`GOOGLE_CLOUD_PROJECT` to the local `.env`, then run `gcloud auth application-default login`.
The `.env` and ADC credential file must never be committed or shared. Google AI Studio API-key
development is also supported by setting `GOOGLE_API_KEY` while Vertex AI is disabled.

Run tests:

```bash
pytest
```

## Privacy and security

- Do not commit credentials, real private messages, or real voicemail files.
- Demo and test assets must be fictional and non-sensitive.
- Uploaded content is processed in memory for the current analysis and is not intentionally retained by the app.
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
