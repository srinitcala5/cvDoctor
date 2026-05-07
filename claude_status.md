# Claude Code — Project Status
_Last updated: 2026-05-08_

---

## Branch

```
main      ← Codex scaffold baseline (CVDOC-7)
  develop ← integration target (no changes yet)
    claude ← all Claude Code work — 2 commits, 27 files, 1147 lines
```

---

## Completed Tasks (claude branch)

| Ticket | Task | Files |
|--------|------|-------|
| CVDOC-9 | Supabase RLS migrations, storage bucket policy, PyJWT middleware, React AuthContext | `supabase/migrations/001–003_*.sql`, `app/utils/auth.py`, `frontend/src/context/AuthContext.tsx`, `frontend/src/lib/supabase.ts` |
| CVDOC-11 | 5-dimension resume scoring prompt + `/resume/score` endpoint | `app/services/scoring.py`, `app/routers/resume.py` |
| CVDOC-13 | JD gap analysis — 2-stage semantic chain + `/jd/gap-analysis` endpoint | `app/services/jd_analysis.py`, `app/routers/jd.py`, `app/models/jd.py` |
| CVDOC-15 | Cover letter generation + scoring + `/cover-letter/generate` endpoint | `app/services/coverletter.py`, `app/routers/coverletter.py`, `app/models/coverletter.py` |
| CVDOC-17 | LinkedIn section scoring + rewrite + `/linkedin/optimise` endpoint | `app/services/linkedin.py`, `app/routers/linkedin.py`, `app/models/linkedin.py` |
| CVDOC-21 | Pitch scoring prompt + `/pitch/score` endpoint | `app/services/pitch_scoring.py`, `app/routers/pitch.py`, `app/models/pitch.py` |
| Deploy | Multi-stage Dockerfile, Azure Container Apps YAML, GitHub Actions PR Overseer | `Dockerfile`, `.azure/container-apps.yaml`, `.github/workflows/pr-overseer.yml`, `.github/scripts/claude_review.py`, `.github/scripts/jira_sync.py` |

---

## Active Endpoints

| Method | Path | Auth required |
|--------|------|---------------|
| POST | `/resume/upload` | No |
| POST | `/resume/score` | Yes (Supabase JWT) |
| POST | `/jd/gap-analysis` | Yes |
| POST | `/cover-letter/generate` | Yes |
| POST | `/linkedin/optimise` | Yes |
| POST | `/pitch/transcribe` | No |
| POST | `/pitch/score` | Yes |
| GET | `/health` | No |

---

## Branch Status

All branches pushed to https://github.com/srinitcala5/cvDoctor.git

- **PR to open:** https://github.com/srinitcala5/cvDoctor/compare/develop...claude
- `gh` CLI not installed — open PR manually via the link above

---

## Pending — Waiting on Codex

| Ticket | Task | Blocks |
|--------|------|--------|
| CVDOC-8 | React + Tailwind frontend scaffold | `frontend/src/` auth files are ready to drop in — need `package.json` / Vite config |
| CVDOC-12 | Score display UI (`ScoreReport.jsx`) | CVDOC-11 backend done |
| CVDOC-14 | Side-by-side diff view UI | CVDOC-13 backend done |
| CVDOC-16 | Cover letter editor + download UI | CVDOC-15 backend done |
| CVDOC-18 | LinkedIn optimizer UI | CVDOC-17 backend done |
| CVDOC-19 | Browser audio recording | — |
| CVDOC-20 | Whisper transcription + WPM | Already delivered in scaffold (`app/services/transcription.py`) |
| CVDOC-21 UI | Pitch feedback display | CVDOC-21 prompt done |

---

## Environment Setup Required

Before testing locally, populate `.env`:

```
ANTHROPIC_API_KEY=        # Anthropic console
OPENAI_API_KEY=           # OpenAI console (Whisper)
SUPABASE_URL=             # Supabase project → Settings → API
SUPABASE_KEY=             # Supabase anon/service key
SUPABASE_JWT_SECRET=      # Supabase project → Settings → API → JWT Secret
```

Run migrations in order via Supabase SQL editor:
1. `supabase/migrations/001_create_tables.sql`
2. `supabase/migrations/002_rls_policies.sql`
3. `supabase/migrations/003_storage_policy.sql`

Start backend: `uvicorn main:app --reload`
API docs: `http://localhost:8000/docs`
