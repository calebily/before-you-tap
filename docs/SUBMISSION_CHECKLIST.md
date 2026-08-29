# Hackathon Submission Checklist

Official deadline: **31 August 2026 at 5:00 PM PDT**  
Sydney equivalent: **1 September 2026 at 10:00 AM AEST**

Target personal deadline: **submit by the evening of 31 August in Sydney**.

## Eligibility and required stack

- [x] Project newly created during the submission period
- [x] Start date recorded: 26 August 2026
- [x] One category selected: The Collaborative Partner
- [x] Gemini 3.5 Flash used through Vertex AI
- [x] Google GenAI SDK used as the Google agent framework
- [x] Cloud Run used as Google Cloud infrastructure
- [x] Application and submission material available in English
- [x] AI coding assistant disclosed
- [x] No pre-existing proprietary code or external dataset incorporated

## Project access and reproducibility

- [x] Public repository: https://github.com/calebily/before-you-tap
- [x] Hosted project: https://before-you-tap-484523463568.australia-southeast1.run.app
- [x] Local spin-up instructions included in README
- [x] Cloud Run deployment instructions included in README
- [x] Architecture diagram created
- [ ] Confirm repository opens in an incognito window
- [ ] Confirm live site opens on desktop and phone in an incognito/private window
- [ ] Confirm `/api/health` reports Gemini 3.5 Flash, Vertex AI, and cloud configured

## Final code freeze

- [ ] Merge the tested security and submission-documentation PR
- [ ] Redeploy the merged `main` branch to Cloud Run
- [ ] Test image selection, multi-image order, camera, audio, analysis, full report, and follow-up
- [ ] Check Cloud Run and Vertex AI spending caps and usage
- [ ] Create the final hackathon release/tag
- [ ] Do not add new features after the freeze; only fix submission-blocking defects

## Demo video

- [ ] Use fictional media only; remove personal browser tabs, notifications, account names, and IDs
- [ ] Record the live Cloud Run site with the `.run.app` address visible
- [ ] Show the agent completing a real image-analysis workflow
- [ ] Show one controlled follow-up action and its adapted instructions
- [ ] Briefly prove saved-audio analysis works
- [ ] Show the architecture diagram
- [ ] Show `/api/health` or Cloud Run/Vertex AI proof without revealing credentials or project IDs
- [ ] State “Gemini 3.5 Flash”, “Google GenAI SDK”, “Vertex AI”, and “Cloud Run” aloud
- [ ] Keep the final video below four minutes
- [ ] Add English narration or English subtitles
- [ ] Upload to YouTube or Vimeo and set the final video to **Public**, not Unlisted
- [ ] Open the final video in an incognito window before submitting

## Devpost form

- [ ] Add the project title and tagline
- [ ] Add the Collaborative Partner category
- [ ] Add the hosted Cloud Run URL
- [ ] Add the public GitHub URL
- [ ] Upload the architecture diagram
- [ ] Add the public demo-video URL
- [ ] Add features and functionality
- [ ] Add technologies used
- [ ] State that no external datasets are used
- [ ] Add findings, challenges, and learnings
- [ ] Answer Google SDK used: Google GenAI SDK for Python
- [ ] Answer project start date: 26 August 2026
- [ ] Confirm README contains reproducible testing instructions
- [ ] Disclose OpenAI Codex as the AI coding assistant
- [ ] Save a draft early and review every field before final submission

## After submission

- [ ] Save screenshots/PDFs of the final Devpost entry and confirmation
- [ ] Keep the linked repository, video, and materials unchanged until judging is complete
- [ ] Keep the public service available or preserve clear deployment proof in the video and repo
- [ ] Monitor billing and Cloud Run usage without changing submission materials
