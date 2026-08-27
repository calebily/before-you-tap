# Before You Tap — MVP Specification v0.2

**Track:** The Collaborative Partner  
**Target submission:** Google Cloud All Things Agentic Hackathon, 31 August 2026, 5:00 PM PDT  
**Product statement:** An AI safety companion that helps older adults analyse suspicious images and audio messages before they tap, reply, pay, call back, or share personal information.

## 1. Problem and user

Scammers impersonate banks, delivery companies, government agencies, friends, and family through emails, text messages, letters, voicemails, and voice messages. Existing security warnings are often technical, alarming, or too vague to act on. Before You Tap gives an older adult a simple way to ask: **“What looks suspicious, and what should I do next?”**

The product must feel like a calm companion, not a cold scanner. It uses plain English, avoids blame and fear, explains uncertainty honestly, and never claims that content is “100% safe” or “definitely a scam.”

## 2. MVP inputs

The web app supports two user-selected analysis modes:

1. **Check images:** Take photos or upload up to five ordered screenshots/photos from the same suspicious text, email, chat, or letter. Initial formats: JPEG, PNG, and WebP, with a 20 MB combined limit.
2. **Check an audio message:** Upload an existing voicemail, voice message, or other audio file that the user has chosen to analyse. Initial formats: MP3, M4A, WAV, OGG, and WebM.

The MVP does **not** listen to live calls, activate the microphone in the background, or intercept phone audio.

## 3. Core user journey

1. The user selects **Check an image** or **Check an audio message**.
2. The interface explains what will be processed and asks the user to choose one or more ordered image pages, or one audio file.
3. The agent verifies that the input is readable or audible enough to assess. If key information is missing, it asks for a clearer file or a short clarification.
4. The agent extracts the relevant content and analyses scam signals, including urgency, secrecy, impersonation, payment or callback requests, suspicious links or phone numbers, remote-access instructions, threats, and requests for passwords, verification codes, banking details, or other private information.
5. The result presents:
   - **Low concern**, **Be careful**, or **High risk**;
   - a one-sentence plain-language summary;
   - the specific warning signs found and where they appeared;
   - uncertainty or missing evidence;
   - two or three safe next steps.
6. The user may ask a follow-up question. The agent keeps the current analysis in session and guides the user without making them start again.

## 4. Agent behaviour and safety contract

- **Low concern:** State that no clear warning signs were found, while making clear that safety cannot be guaranteed. Recommend independent verification before sharing sensitive information.
- **Be careful:** Identify suspicious or uncertain details, advise the user not to rush, and ask for more evidence when that would materially improve the assessment.
- **High risk:** Clearly advise the user not to tap, reply, call the supplied number, transfer money, install software, or share passwords or verification codes. Suggest independently contacting the organisation through a known official channel or speaking with a trusted person.
- Distinguish observed evidence from assumptions. Never invent sender identities, URLs, phone numbers, transcripts, or official contact information.
- If an image is incomplete, audio is unclear, or the file is unsupported or unrelated, request a better input instead of forcing a risk classification.
- Treat the result as decision support, not a definitive fraud determination.

## 5. Accessibility and privacy

- Large text, high contrast, 48×48 px minimum touch targets, keyboard navigation, and screen-reader labels.
- Risk is communicated with words and icons, not colour alone.
- One primary action per screen; short, plain-English instructions; no countdowns or fear-based wording.
- Whenever the user must press a control, the next required button or icon is visibly framed with a persistent high-contrast border or filled container, paired with a text label and clear instruction. Guidance must not rely on colour, animation, or an icon alone.
- Users explicitly choose every file. The interface states that content will be processed by a cloud AI service.
- Uploaded files and generated transcripts are used only for the current analysis and are not intentionally retained after the session in the MVP.
- Demo and test assets contain fictional, non-sensitive information. No real private voicemail or personal data is committed to the repository.

## 6. Technical scope

- **Interface:** Responsive web app with image capture/upload and audio-file upload.
- **Backend:** Python, FastAPI, and Google Agent Development Kit (ADK).
- **Model:** Gemini 3.5 Flash multimodal through Vertex AI for image/audio understanding and risk reasoning.
- **Google Cloud:** Cloud Run for deployment and visible proof of the cloud backend.
- **Session state:** In-memory state initially; Firestore only if needed for reliable multi-turn sessions.
- **Security:** Validate file type and size; keep secrets out of the frontend and repository; use environment variables or managed cloud configuration for credentials.

## 7. MVP acceptance criteria

The MVP is complete when a judge can:

1. Upload one or more ordered images from the same suspicious content and receive a combined evidence-based risk assessment with safe next steps.
2. Upload a suspicious voicemail or voice message and receive the same structured assessment.
3. See a helpful clarification request for an unreadable image or unclear audio file rather than a fabricated result.
4. Ask a follow-up question that uses the current session context.
5. Use the interface on desktop and mobile with accessible controls.
6. See the working backend deployed on Cloud Run in the demo video.

## 8. Out of scope and future vision

The MVP excludes live-call monitoring, background microphone access, native phone-call interception, native share extensions, Gmail integration, user accounts, long-term personal memory, automatic blocking/reporting, contacting family members, and enterprise multi-agent infrastructure.

**Future vision:** A privacy-reviewed, user-controlled conversation safety mode that can recognise escalating scam tactics during a call and warn the user before they share information or take financial action.

## 9. Demo scenario

The demo shows two inputs: a fake bank-security screenshot and a fictional voicemail requesting an urgent callback and verification details. Before You Tap identifies the concrete warning signs, returns **High risk**, explains its reasoning in plain language, and guides the user to pause and contact the bank independently through an official channel.
