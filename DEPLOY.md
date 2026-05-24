# Deploying IncidentIQ 🚀

**Recommended:** Render (backend) + Vercel (frontend). Both free, both deploy
directly from GitHub. ~10 minutes total.

---

## Part 1 — Deploy backend to Render

1. Go to **https://render.com** → sign in with GitHub
2. Click **New → Web Service**
3. Connect your GitHub and select **`Tanya-garg10/IncidentIQ`**
4. Render will auto-detect the `render.yaml` blueprint. Click **Apply**.
   - If it doesn't, fill in manually:
     - **Root Directory:** `backend`
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Once the service is created, open the **Environment** tab and add:
   - `GROQ_API_KEY` = `gsk_your_real_key` (the new one you rotated)
   - `LLM_PROVIDER` = `groq`
   - `GROQ_MODEL` = `llama-3.3-70b-versatile`
   - `INCIDENTIQ_DB_PATH` = `/tmp/incidents.db`
6. Click **Manual Deploy → Deploy latest commit**
7. Wait ~3 min. You'll get a URL like `https://incidentiq-backend.onrender.com`
8. Test: open `https://incidentiq-backend.onrender.com/` — should return
   `{"message":"IncidentIQ Backend Running","version":"0.3.0"}`

> ⚠️ Free tier sleeps after 15 min of inactivity. First request after
> sleep takes ~30 sec to wake up. For a live demo, hit the URL once a few
> minutes before showing it.

---

## Part 2 — Deploy frontend to Vercel

1. Go to **https://vercel.com** → sign in with GitHub
2. Click **Add New → Project**
3. Import **`Tanya-garg10/IncidentIQ`**
4. **Root Directory:** click **Edit** → choose `frontend`
5. **Framework Preset:** Next.js (auto-detected)
6. Expand **Environment Variables** and add:
   - `NEXT_PUBLIC_API_BASE` = `https://incidentiq-backend.onrender.com`
     (use the URL from step 7 of Part 1)
   - `NEXT_PUBLIC_WS_BASE` = `wss://incidentiq-backend.onrender.com`
     (note: `wss://` not `ws://` for HTTPS sites)
7. Click **Deploy**
8. Wait ~2 min. You'll get `https://incidentiq.vercel.app` (or similar).

That's it — open the Vercel URL and your dashboard is live.

---

## Part 3 — Smoke test the deployment

After both are up:

1. Visit your Vercel URL
2. Logs should be streaming live (WebSocket connected badge)
3. Click **🔥 Simulate Incident** — analysis card should refresh
4. Open the chat panel and ask a question — engine badge should say `groq`

If anything fails:
- **Backend not responding:** check Render logs in dashboard
- **CORS errors in browser console:** confirm Vercel env var matches backend URL
- **WebSocket not connecting:** ensure `NEXT_PUBLIC_WS_BASE` uses `wss://`
- **Engine says rule-based:** the `GROQ_API_KEY` env var on Render is missing or wrong

---

## Alternative: Docker on a VPS

If you have a server (DigitalOcean, AWS EC2, etc.) and want a single deploy:

```bash
git clone https://github.com/Tanya-garg10/IncidentIQ.git
cd IncidentIQ
echo "GROQ_API_KEY=gsk_your_key" > docker/.env
cd docker
docker compose --env-file .env up -d --build
```

App on `http://your-server-ip:3000`, API on `:8000`.

---

## Future-proofing

When ready, swap to:
- **Database:** Supabase or Neon (real Postgres) instead of SQLite
- **Frontend:** keep Vercel
- **Backend:** Render Pro ($7/mo for no sleep) or Fly.io
