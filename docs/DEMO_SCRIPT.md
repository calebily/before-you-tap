# Demo Video Plan and Narration

Target length: **3 minutes 30 seconds to 3 minutes 50 seconds**. The final upload must remain under
four minutes.

## What the judges must see

1. The real public Cloud Run website, with the `.run.app` URL visible.
2. A real multimodal Gemini request completing, not a mockup.
3. The agent examining evidence, returning a typed risk result, and choosing relevant follow-up
   actions.
4. One follow-up branch adapting to what the user says they already did.
5. Brief proof that saved-audio analysis works.
6. The architecture diagram and proof of Gemini 3.5 Flash, Vertex AI, and Cloud Run.

The strongest primary case is the two-page **fictional Harbourline Bank** message. It demonstrates
multi-image ordering, evidence extraction, High risk classification, and the **I clicked the link**
follow-up. The fictional delivery voicemail is a short second case that proves audio support. The
Low concern reminder is a backup and can appear for two or three seconds in a closing montage.

## Recording preparation

- Use a clean browser profile or incognito window.
- Hide bookmarks and close unrelated tabs.
- Turn on Do Not Disturb and disable browser/password-manager pop-ups.
- Use fictional demo assets only.
- Keep the Cloud Run URL visible when practical.
- Preload the assets in a Finder folder so file selection is quick.
- Test every asset immediately before recording and note the result Gemini returns.
- Record short clips, but preserve the real upload-to-result sequence.
- Cut loading time; never splice in a result produced from different input.
- Do not show Google account pages, billing details, project IDs, API keys, terminal history, or
  Application Default Credential locations.

## Timed storyboard and script

### 0:00–0:12 — Cold open: show the outcome first

**Screen:** Start on the completed High risk result. Show the red risk label, short summary, and
first safe next step. Keep the Cloud Run domain visible.

**Narration:**

> This is Before You Tap. It turns a suspicious message into a clear risk warning and the next safe
> action, before someone clicks, calls back, pays, or shares private information.

### 0:12–0:38 — Problem and value

**Screen:** Cut to the top of the homepage. Briefly show the image and audio choices and the large,
mobile-first controls.

**Narration:**

> Hi, I’m Lily. Scam messages often work by creating urgency before a person has time to verify
> what they are being told. For many older adults, existing security warnings are technical or too
> vague to act on. Before You Tap is a calm, multimodal safety companion that explains the evidence
> in plain English and guides the user one step at a time.

### 0:38–1:08 — Begin a real multi-image check

**Screen:** Select **Photo or screenshot**. Add `high-risk-bank-page-1.png` and
`high-risk-bank-page-2.png`. Briefly show the two ordered previews, then press **Check these
images**. Cut only the waiting time.

**Narration:**

> This is the live application running on Google Cloud Run. I’ll upload two screenshots from one
> fictional bank message. Before sending anything to the model, the backend checks the file count,
> total size, MIME type, and file signature. The pages remain in the user’s chosen reading order.

### 1:08–1:50 — Show autonomous analysis

**Screen:** Show the High risk result, summary, at least two warning signs, uncertainty, and safe
next steps. Expand **See the full report** briefly.

**Narration:**

> Gemini 3.5 Flash reads both pages together. The agent identifies the account-lock threat, the
> request for a verification code, the so-called safety-account transfer, and the instruction to
> keep the request secret. It separates observed evidence from uncertainty, returns a structured
> High risk result, and places the safest immediate action first. It never claims that a message is
> definitely safe or definitely fraudulent.

### 1:50–2:25 — Show the guided follow-up workflow

**Screen:** Scroll to the follow-up choices and select **I clicked the link**. Show the adapted
result and its ordered protective steps.

**Narration:**

> This is more than a one-off warning. Based on the evidence, the agent chooses only relevant
> follow-up options. If the user says they already clicked the link, it changes the guidance to the
> next safest actions without blaming them. For data minimisation, the follow-up sends only the
> structured assessment and the selected action. The original screenshots are not sent again.

### 2:25–2:55 — Prove saved-audio support

**Screen:** Select **Check an audio message**, choose the fictional delivery voicemail, play one or
two seconds, then show its completed result. Cut the model waiting time.

**Narration:**

> The same workflow also accepts a saved voicemail or voice message. It does not listen to live
> calls and never turns on the microphone in the background. Here, Gemini detects an unverified
> caller, urgency, and a suspicious callback request, then returns a cautious next step.

### 2:55–3:25 — Architecture and production proof

**Screen:** Show `docs/architecture.svg`, then open the public `/api/health` endpoint. Keep the JSON
long enough to read `gemini-3.5-flash`, `vertex_ai`, and the configured booleans.

**Narration:**

> The application uses the Google GenAI SDK for Python, Gemini 3.5 Flash on Vertex AI, FastAPI, and
> Cloud Run. Uploaded media is processed in memory and is not intentionally retained. Model output
> must pass a strict response schema before the interface displays it, and no API key is exposed in
> the browser.

### 3:25–3:45 — Close

**Screen:** Return to the homepage or show a fast three-result montage: High risk, Be careful, and
Low concern.

**Narration:**

> Before You Tap does not replace a bank or fraud investigator. It creates a calm pause at the
> moment pressure is highest, explains what stood out, and helps a person take the next safer step.

## Editing rules

- Keep the final video below four minutes.
- Jump cuts, captions, and removal of waiting time are fine.
- Keep each model result paired with the exact input that produced it.
- Do not add fake cursor clicks, fake results, or a mock Cloud Run screen.
- Add English captions even though the narration is English.
- Upload early, check the final video in an incognito window, and set it to **Public** before
  submitting the Devpost URL.
