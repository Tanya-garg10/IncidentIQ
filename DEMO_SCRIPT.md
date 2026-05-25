# IncidentIQ ΓÇö 3-minute Demo Video Script ≡ƒÄ¼

A tight, judge-friendly script. Total runtime Γëñ 3:00. Every second is timed.

---

## Pre-recording checklist (do BEFORE you hit record)

1. Γ£à Open the dashboard URL (Vercel) in a clean browser window
2. Γ£à Wait 30 sec ΓÇö confirm "live logs" badge says **ΓùÅ connected**
3. Γ£à Hit `https://incidentiq-backend-gw17.onrender.com/` in another tab
   first, so Render has woken up (free tier sleeps after 15 min)
4. Γ£à Close all unrelated tabs / notifications / Slack etc.
5. Γ£à Set browser zoom to 100% (or 110% for visibility)
6. Γ£à Bottom of dashboard should show no red errors
7. Γ£à Have these ready in Notepad to copy-paste during chat demo:
   - "Why did payment-service crash?"
   - "What should I do to fix this?"

Recording app: **OBS Studio** (free) or **Loom** (easiest, browser-based).

---

## ≡ƒÄ¼ The Script (timed)

### [0:00 ΓÇô 0:20] HOOK ΓÇö set the problem
**Show:** your face on webcam OR a slide saying _"It's 2:47 AM"_

> "It's 2:47 AM. Production crashes. Your phone explodes with PagerDuty alerts.
> You're staring at thousands of cryptic log lines, trying to figure out what
> broke, why, and how to fix it ΓÇö fast.
>
> What if AI could do that for you? Meet **IncidentIQ**."

**[Cut to dashboard]**

---

### [0:20 ΓÇô 0:40] DASHBOARD INTRO ΓÇö what it is
**Show:** the live dashboard. Mouse hovers over each section briefly.

> "IncidentIQ is an AI-powered incident analysis platform.
> On the left, **live log streams from four services** ΓÇö auth, payment, user,
> and the API gateway ΓÇö flowing in real-time over WebSockets.
>
> Right now everything's healthy. Watch what happens when production breaks."

**Point at:** Live Log Stream ΓåÆ Service Health (all green) ΓåÆ Severity meter (Low)

---

### [0:40 ΓÇô 1:10] SIMULATE THE OUTAGE
**Click:** ≡ƒÜÇ **Mark Deployment** (small button, top right)

> "First, I'll simulate a fresh deployment of payment-service v2.4.1.
> Common scenario ΓÇö a release just shipped."

**Click:** ≡ƒöÑ **Simulate Incident** (the big glowing button)

> "Now production breaks."

**Wait 2 seconds. Logs flood in. Point at:**
- Red CRITICAL badges streaming in the log panel
- Severity meter sliding from green ΓåÆ red **Critical**
- Service Health: payment-service drops to **DOWN** with pulsing red dot

> "In two seconds: severity jumps to critical, payment-service is down,
> health score drops to thirty out of a hundred."

---

### [1:10 ΓÇô 1:40] AI ANALYSIS ΓÇö the killer moment
**Scroll down to the Active Incidents card.** Hold for 3 sec on each card.

> "And here's where the AI kicks in. **Powered by Groq's Llama model**,
> IncidentIQ doesn't just match keywords ΓÇö it reads the logs and explains them.
>
> It's identified four incidents, the root cause for each, and a specific
> recommended fix. _'Optimize database queries and increase CPU resources.'_
> _'Inspect stack trace, restart the service.'_
>
> This is what an SRE does in their head ΓÇö generated in three seconds."

**Point at the Anomaly Detection card:**
> "On the right, anomaly detection caught the error-rate spike.
> And ΓÇö this is my favorite part ΓÇö a **predictive alert**:
> _'Likely service degradation within fifteen minutes.'_"

**Point at the deployment correlation banner:**
> "It even correlated the incident with the deployment we just made.
> _'Issue began two minutes after payment-service v2.4.1 deploy. Consider rollback.'_"

---

### [1:40 ΓÇô 2:15] CHAT WITH YOUR INFRA ≡ƒñû
**Scroll to ChatPanel, click into the input.**

> "But what if I want to ask a follow-up question? IncidentIQ lets you
> **chat with your infrastructure**."

**Type:** `Why did payment-service crash?` ΓåÆ press Enter

**Wait for the streaming answer (~2 sec).**

> "It's reading my actual logs in real-time and answering with full context.
> No hallucination ΓÇö grounded in the data on screen."

**Type one more:** `What should I do to fix this?` ΓåÆ press Enter

**Wait for response.**

> "Concrete, actionable, prioritized steps. Like having a senior SRE on call,
> 24/7."

---

### [2:15 ΓÇô 2:40] REPORT EXPORT + TECH STACK
**Click:** Γ¼ç **Report** button. Markdown file downloads.

> "When the incident's resolved, click Report and it downloads a clean
> markdown postmortem ΓÇö incident summary, timeline, services affected,
> recommended fixes ΓÇö ready to paste into Notion or share with your team."

**Open the downloaded file briefly OR cut to a slide showing it.**

> "Under the hood: **FastAPI** backend with WebSockets, **Next.js 14**
> frontend with Tailwind and Framer Motion, **Groq** for the AI layer,
> **SQLite** for incident history, deployed on **Render and Vercel**."

---

### [2:40 ΓÇô 3:00] CLOSE ΓÇö the vision
**Cut back to dashboard, full screen.**

> "IncidentIQ turns hours of 2 AM panic into seconds of clarity.
>
> Live monitoring. AI root cause. Predictive alerts. Deployment correlation.
> Chat with your infrastructure.
>
> All in one dashboard. **This is what production debugging should feel like
> in 2026.**
>
> Thanks for watching."

**[End screen with GitHub URL + live demo link]**
- `github.com/Tanya-garg10/IncidentIQ`
- live demo URL

---

## ΓÅ▒ Time Budget Cheat Sheet

| Section | Length | Cumulative |
|---------|--------|-----------|
| Hook | 0:20 | 0:20 |
| Dashboard intro | 0:20 | 0:40 |
| Simulate outage | 0:30 | 1:10 |
| AI analysis | 0:30 | 1:40 |
| Chat demo | 0:35 | 2:15 |
| Report + stack | 0:25 | 2:40 |
| Close | 0:20 | 3:00 |

---

## Pro tips for a winning recording

1. **Speak clearly, slightly slower than normal.** Judges watch hundreds of
   demos ΓÇö clarity beats speed.
2. **Pre-warm Render** by visiting the URL 2 min before recording. Otherwise
   the first hit takes ~30 sec to wake.
3. **Record at 1080p**, not 4K. Smaller file, no quality loss for screen.
4. **Cursor highlighter:** turn on "Show mouse clicks" in OBS so judges
   see what you click.
5. **Cut hard between scenes** ΓÇö no dead air, no "umm". If you mess up,
   pause 2 sec, re-do that line, edit out the bad take.
6. **Background music:** a soft instrumental at -25dB makes a huge
   difference. Try Lofi Geek or Audionautix on YouTube Audio Library
   (royalty-free).
7. **First 10 seconds matter most.** Hook them with the 2 AM line, not
   a tech logo intro.
8. **Captions/subtitles** boost watch time by ~30%. Loom and CapCut both
   auto-generate them in 1 click.

---

## Alternative: 60-second elevator cut

If you need a shorter version (e.g. for Twitter/LinkedIn):

> _"Production crashes at 2 AM. Most teams find out from angry tweets.
> IncidentIQ uses AI to read your logs, identify the root cause, predict
> failures before they happen, and tell you exactly how to fix them ΓÇö
> in seconds. Live demo: [URL]"_

Show: simulate incident ΓåÆ AI analysis card ΓåÆ chat ΓåÆ done.
