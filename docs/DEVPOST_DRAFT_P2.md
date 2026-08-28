# Devpost Draft P2 — Natural Version

## Project name

Before You Tap

## Tagline

Check a suspicious message before you click, call back, pay, or share personal details.

## Category

The Collaborative Partner

## Project start date

26 August 2026

## Inspiration

Many scam messages are not technically complicated. They work because they make the person feel
rushed or scared. They might say that a bank account will be locked, a parcel cannot be delivered,
or a family member needs money immediately.

I started thinking about what happens when an older person receives one of these messages and is
not sure what to do. A warning that only says “be careful” is not very helpful, while a long
security report can be difficult to read. I wanted to make something that points out what looks
wrong and gives the person a clear next step before they act.

## What it does

Before You Tap is a mobile-friendly website for checking suspicious screenshots, photos,
voicemails, and saved voice messages.

The user can:

- take a photo;
- upload or paste up to five screenshots from the same message;
- put those screenshots in the correct reading order; or
- choose a saved audio file.

Gemini checks the supplied content and returns one of three results: **Low concern**,
**Be careful**, or **High risk**. The short result appears first, together with what the user
should do now. A full report is available for anyone who wants to see the warning signs, the
evidence behind them, and what the app cannot confirm.

The app then asks whether the user has already done something, such as clicking the link, calling
the sender, sharing personal details, or sending money. Gemini chooses only the follow-up buttons
that fit the message. When the user selects one, the app gives the next steps for that situation
instead of opening an unrestricted chat.

The app does not listen to live calls, turn on the microphone in the background, or claim that it
can prove a message is safe or fraudulent.

## How I built it

The frontend uses HTML, CSS, and JavaScript. I kept the page simple, with large buttons, strong
contrast, camera access on supported phones, drag and drop, pasted screenshots, ordered image
previews, audio playback, keyboard support, and optional browser read-aloud.

The backend is built with FastAPI. Before a file is sent for analysis, it checks the number of
files, total size, MIME type, and file signature. This helps reject an unsupported or misleading
upload before it reaches the model.

The backend uses the Google Gen AI SDK for Python to send images or audio to Gemini 3.5 Flash
through Vertex AI. Gemini returns the risk level, summary, warning signs, uncertainty, next steps,
and relevant follow-up choices in a fixed format. Pydantic checks that result before it is shown
on the page.

The app runs in a container on Google Cloud Run. It uses Google Cloud service identity, so there
is no Gemini API key in the browser. Uploaded files are handled in memory and Before You Tap does
not intentionally store them. The MVP also has no user account or database.

## Google technologies used

- Gemini 3.5 Flash
- Vertex AI
- Google Gen AI SDK for Python
- Google Cloud Run
- Google Cloud service identity and Application Default Credentials

## Other technologies used

- Python 3.12
- FastAPI and Uvicorn
- Pydantic and pydantic-settings
- HTML, CSS, and JavaScript
- Pytest
- Docker

## Data sources

No external dataset is used. The app analyses only the images or audio selected by the user for
that check, together with the instructions in the application. The materials used in the demo are
fictional and do not contain real personal or financial information.

## Challenges

The biggest challenge was deciding how much information to show. My first version looked more like
a normal security report. It worked, but it had too much text for the people I was designing for.
I changed the page so that the risk level and the most important action appear first. The user can
open the full report only if they want more detail.

I also did not want the follow-up to become a general chatbot. Too many choices could make the user
more confused or encourage them to type more private information. Instead, Gemini reads the result
and chooses a small number of buttons that match what happened.

Handling several screenshots was another challenge. They need to stay in the order chosen by the
user and they should all belong to the same email or conversation. Saved audio also has several
possible file types, so both the browser and backend need to check the upload carefully.

Finally, the app needs to be useful without sounding certain when it cannot know who really sent a
message. The result therefore separates visible or audible warning signs from things that cannot
be confirmed.

## Accomplishments I am proud of

- The same website works with camera photos, several ordered screenshots, and saved audio.
- The short result is easy to find, while the supporting explanation is still available.
- Follow-up steps change according to what the user says they have already done.
- The original image or audio is not sent again during the follow-up.
- The public Cloud Run site uses Vertex AI without exposing an API key in the frontend.
- The project has automated tests for upload checks, image and audio analysis, follow-up rules,
  configuration, API behaviour, and browser security controls.

## What I learned

I learned that designing for an older user is not only about making the font and buttons bigger.
The order of information matters just as much. The first thing on the result page should answer:
“Should I stop?” and “What should I do now?” The explanation can come afterwards.

I also learned that an agent does not have to look like an open chat window. In Before You Tap,
Gemini reads the evidence, decides which warning signs matter, chooses the next actions, and changes
the instructions after the user says what has already happened.

On the technical side, I learned how to send image and audio input through Vertex AI, validate a
fixed model response, deploy a container to Cloud Run, and use Google Cloud credentials without
putting a secret key in the browser.

## What is next

I deliberately left out live-call monitoring because it raises consent, recording-law, and privacy
questions. A future version could add local redaction before a file is uploaded, a phone share
extension, a way to find a verified official contact, and an opt-in option to contact a trusted
family member or friend after a High risk result.

## AI assistance

I used OpenAI Codex to help write and review code and documentation. I chose the problem, decided
how the product should work, reviewed the safety and privacy decisions, and tested the final
flows. The project was started during the hackathon and does not reuse an earlier proprietary
project or external dataset.

## Testing instructions

1. Open the hosted Cloud Run URL on a current desktop or mobile browser.
2. Choose **Photo or screenshot** or **Check an audio message**.
3. Select fictional, non-sensitive media within the size limits shown on the page.
4. Press the check button and wait for the result.
5. Open the full report and choose one of the follow-up buttons.

No login is required. Local setup and Cloud Run deployment instructions are included in the
repository README.
