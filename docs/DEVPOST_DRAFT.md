# Devpost Submission Draft

## Project name

Before You Tap

## Tagline

A simple way to check suspicious messages and voice notes before responding, paying, or sharing details.

## Category

The Collaborative Partner

## Project start date

26 August 2026

## Inspiration

Many scams do not begin with sophisticated malware. They begin with a message or voicemail that
creates urgency, fear, secrecy, or confusion. The target is pressured to click a link, call an
unverified number, share a verification code, or move money before they have time to ask someone
they trust.

Existing warnings are often technical, alarmist, or too vague to be useful. I wanted to build a
clear guidance for older adults: something that does not shame the user, does not pretend to
offer certainty, and turns suspicious content into a small number of safe, understandable actions.

## What it does

Before You Tap is a mobile-first web agent for checking suspicious images and saved audio messages.
The user can take a photo, upload or paste up to five ordered screenshots from one email or
conversation, or choose an existing voicemail or voice message.

The agent autonomously checks whether the content is usable and related, extracts the visible or
audible evidence, assesses common manipulation and scam signals, and returns a structured result:

- Low concern, Be careful, or High risk;
- a short plain-English summary;
- the specific warning signs and evidence;
- uncertainty and missing context;
- immediate safe next steps; and
- only the guided follow-up actions relevant to the situation.

The result prioritises what the user should do next. If the user says they already clicked a link,
called the sender, shared private information, or sent money, the agent uses the existing structured
assessment to provide the next protective steps. The original media is not resent during this
follow-up.

Before You Tap does not monitor live calls, activate the microphone in the background, claim that a
message is definitely safe, or replace a bank, law-enforcement agency, or fraud investigator.

## How I built it

The responsive frontend is written in HTML, CSS, and JavaScript with large touch targets,
high-contrast controls, keyboard support, screen-reader labels, optional browser read-aloud, camera
capture, drag-and-drop, clipboard image input, ordered multi-image previews, and saved-audio
playback.

The Python FastAPI backend validates file count, size, MIME type, and file signatures before model
analysis. It uses the Google GenAI SDK for Python to send image or audio input to Gemini 3.5 Flash
through Vertex AI. Gemini is constrained to return a typed schema containing the risk level,
evidence, uncertainty, safe steps, and allowed follow-up actions. Pydantic validates this output
before the frontend renders it.

The application is packaged in a container and deployed to Google Cloud Run. It uses Cloud service
identity rather than placing a Gemini key in the browser. Current assessment state remains only in
the active browser page; the MVP has no database or long-term user memory.

## Google technologies used

- Gemini 3.5 Flash
- Vertex AI
- Google GenAI SDK for Python
- Google Cloud Run
- Google Cloud service identity / Application Default Credentials

## Other technologies used

- Python 3.12
- FastAPI and Uvicorn
- Pydantic and pydantic-settings
- HTML, CSS, and JavaScript
- Pytest
- Docker

## Data sources

No external datasets are used. The agent analyses only the media explicitly selected by the user
for the current check, together with the safety instructions defined in the application. All demo
media is fictional and contains no real personal or financial information.

## Challenges

The most difficult design decision was balancing useful guidance with privacy and accessibility.
A free-form chatbot could easily overwhelm an older user or encourage them to paste more sensitive
information. Instead, the model chooses a small set of controlled follow-up actions based on the
evidence, and the interface reveals detail progressively.

Multimodal input also required careful validation. Browser-reported MIME types are not enough, so
the backend verifies both the declared type and the file signature. Multi-image input must preserve
reading order while detecting unrelated pages, and audio aliases need to be normalised for model
processing.

Finally, scam detection must communicate uncertainty honestly. The prompts and schemas prevent
absolute safety claims, distinguish evidence from assumptions, and require a safer independent
verification path.

## Accomplishments I am proud of

- One accessible workflow supports camera images, ordered multi-page screenshots, and saved audio.
- The agent returns evidence-based, schema-validated results rather than an unrestricted block of
  model text.
- Guided follow-up adapts to what the user has already done without resending the original media.
- The interface places the short result and immediate action before the full technical report.
- The Cloud Run deployment uses Vertex AI without exposing a frontend API key.
- Automated tests cover validation, image and audio orchestration, follow-up constraints,
  configuration, API behaviour, and browser-security controls.

## What I learned

Building for a vulnerable user changes what “good AI UX” means. More detail is not always more
helpful. A clear risk word, one calm sentence, and the next safe action need to come before the
explanation. Progressive disclosure lets the user stop when they have enough information while
still giving judges, family members, or support workers access to the full reasoning.

I also learned that agentic behaviour does not require an open-ended chat interface. In this
project, the important behaviour is the decision pipeline: interpreting multimodal evidence,
selecting relevant actions, preserving structured session context, and adapting the safety workflow
to the user’s feedback.

## What is next

The MVP intentionally avoids live-call monitoring, automatic reporting, user accounts, and
long-term memory. A future version could add a privacy-reviewed native share extension, local
redaction of sensitive fields before cloud processing, verified official-contact retrieval, and an
explicit opt-in trusted-contact workflow. Any live conversation feature would require careful
consent, recording-law, privacy, and safety review before development.

## Reuse and AI-assistance disclosure

Before You Tap was newly created during the hackathon submission period. OpenAI Codex was used as
an AI coding assistant. Product direction, safety decisions, review, testing, and the final
submission remain my responsibility. No pre-existing proprietary project code or external dataset
was incorporated.

## Testing instructions

1. Open the hosted Cloud Run URL in a current desktop or mobile browser.
2. Choose **Photo or screenshot** or **Check an audio message**.
3. Use fictional, non-sensitive media within the displayed format and size limits.
4. Submit the file and wait for the structured risk result.
5. Expand the full report, then select one guided follow-up action.

No login is required. Reproducible local and Cloud Run setup instructions are in the repository
README.
