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
> step, before someone clicks, calls back, pays, or shares private information.

### 0:12–0:38 — Problem and value

**Screen:** Cut to the top of the homepage. Briefly show the image and audio choices and the large,
mobile-first controls.

**Narration:**

> Hi, I’m Lily. I built this because scam messages usually do not give people much time to think.
> They say an account will be locked, a parcel is waiting, or someone needs money urgently. That
> pressure can be especially difficult for older adults, and a warning that only says “be careful”
> is not very useful. I wanted the app to show what looks suspicious and give the user a clear next
> step.

### 0:38–1:08 — Begin a real multi-image check

**Screen:** Select **Photo or screenshot**. Add `high-risk-bank-page-1.png` and
`high-risk-bank-page-2.png`. Briefly show the two ordered previews, then press **Check these
images**. Cut only the waiting time.

**Narration:**

> This is the real app running on Google Cloud Run. I’m using two fictional screenshots from the
> same bank message. The user can check the pages and put them in the right order. Before the files
> reach Gemini, the backend checks that they are valid images and checks the file count and total
> size.

### 1:08–1:50 — Show autonomous analysis

**Screen:** Show the High risk result, summary, at least two warning signs, uncertainty, and safe
next steps. Expand **See the full report** briefly.

**Narration:**

> Gemini 3.5 Flash reads both pages together. Here, it notices the threat to lock the account, the
> request for a security code, the transfer to a so-called safety account, and the instruction not
> to tell anyone. It explains each warning sign, shows what it cannot confirm, and puts the most
> important action at the top. It does not pretend that it can prove who sent the message.

### 1:50–2:25 — Show the guided follow-up workflow

**Screen:** Scroll to the follow-up choices and select **I clicked the link**. Show the adapted
result and its ordered protective steps.

**Narration:**

> The app does not stop after showing a risk level. It asks what has already happened and only shows
> choices that make sense for this message. If I choose “I clicked the link,” the instructions
> change to what I should do now. The original screenshots are not sent again for this follow-up;
> only the result and the answer I selected are used.

### 2:25–2:55 — Prove saved-audio support

**Screen:** Select **Check an audio message**, choose the fictional delivery voicemail, play one or
two seconds, then show its completed result. Cut the model waiting time.

**Narration:**

> The app can also check a saved voicemail or voice message. It does not listen to live calls and
> it does not turn on the microphone in the background. In this example, the caller creates
> urgency and asks the user to call an unverified number, so the app tells them to check through an
> official source instead.

### 2:55–3:25 — Architecture and production proof

**Screen:** Show `docs/architecture.svg`, then open the public `/api/health` endpoint. Keep the JSON
long enough to read `gemini-3.5-flash`, `vertex_ai`, and the configured booleans.

**Narration:**

> Behind the app, I use the Google Gen AI SDK for Python, Gemini 3.5 Flash on Vertex AI, FastAPI,
> and Cloud Run. The uploaded files are handled in memory and are not intentionally stored. The
> model has to return the result in a fixed structure before the website can display it, and there
> is no API key in the browser.

### 3:25–3:45 — Close

**Screen:** Return to the homepage or show a fast three-result montage: High risk, Be careful, and
Low concern.

**Narration:**

> Before You Tap cannot prove that every message is safe or fake. My goal is simpler: when someone
> is being rushed, give them a moment to check what is happening before they do anything.

## Editing rules

- Keep the final video below four minutes.
- Jump cuts, captions, and removal of waiting time are fine.
- Keep each model result paired with the exact input that produced it.
- Do not add fake cursor clicks, fake results, or a mock Cloud Run screen.
- Add English captions even though the narration is English.
- Upload early, check the final video in an incognito window, and set it to **Public** before
  submitting the Devpost URL.
