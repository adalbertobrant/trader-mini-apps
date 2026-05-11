# Project: AI-Driven SEO & Content Agency Engine

## Project Vision
Automate the research-to-revenue pipeline by building a specialized content agency engine. Covers SEO-optimized articles, conversion-focused product descriptions, and personalized sales outreach.

## Operational Mandates
1. **Security First:** NEVER commit API keys, secrets, or sensitive data. All credentials must reside in `.env` (git-ignored). Use `pydantic-settings` for secure configuration management. Zero-leak policy: no keys in logs, code, or version control.
2. **Consensus Requirement:** All critical outputs (keywords, outlines, copy, emails) MUST use at least 3 AI models synthesized into one "Gold Standard" result via `ConsensusSynthesizer`.
3. **Async First:** All AI client calls MUST be async. Use `AsyncAnthropic`, `AsyncGroq`, `AsyncOpenAI`, and `complete_async` (Mistral). Never use sync clients inside async methods — it blocks the event loop.
4. **True Concurrency:** Use `asyncio.gather(*tasks, return_exceptions=True)` when running multiple coroutines in parallel. Never `await` in a sequential loop when tasks are independent.
5. **Kanban Management:** All tasks MUST be tracked in `BACKLOG.md`. Max 1-2 tasks In Progress at a time.
6. **Test Everything:** Every module must have a corresponding test in `tests/`. Tests use mocks — no real API calls. Run `python -m pytest` before every commit.
7. **Document Everything:** Every session must be logged in `DIARY.md`. Architecture decisions go in `HISTORY.md`. Roadmap lives in `build_plan.md`.
8. **Git Discipline:** Commit after every completed feature, fix, or doc update. Use conventional commit messages (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

## Tech Stack
- **AI Orchestration:** Multi-Model (Anthropic Claude, Google Gemini, Groq/LLaMA, Mistral, OpenRouter, LocalAI/Ollama)
- **Search:** Tavily API (real-time SERP context)
- **Framework:** Python 3.10+
- **Config:** pydantic-settings (`.env`-based, secure)
- **CLI:** `main.py` (asyncio + stdlib)
- **Testing:** pytest + pytest-mock + pytest-asyncio
- **API (next):** FastAPI + Uvicorn

## Current Project State (as of 2026-04-14)
| Phase | Status | Entry Point |
|---|---|---|
| Infrastructure | ✅ Done | `src/utils/` |
| Phase 1 — Research | ✅ Done | `src/research/market_analyzer.py` |
| Phase 2 — Content | ✅ Done | `src/content/seo_writer.py` |
| Phase 3 — Marketing | ✅ Done | `src/marketing/` |
| Phase 4 — CLI | ✅ Done | `main.py` |
| Async Compliance | ✅ Done | All modules fully async (incl. Tavily) |
| Input Sanitization | ✅ Done | `src/utils/prompt_template.py` |
| Phase 5 — REST API | 🔜 Next | FastAPI (not started) |
| Phase 6 — Integrations | 🔜 Planned | WordPress, Shopify, Mercado Livre, OLX, Make.com, Zapier |

## Handoff: Ready to Start Phase 5
All pre-conditions for Phase 5 are defined in `BACKLOG.md` under "Pre-conditions (security — must be resolved first)".
Start there before writing any FastAPI code. Do NOT skip the pre-conditions.

### Mandatory first steps for Phase 5:
1. Design API key auth strategy (storage, rotation, scoping)
2. Add rate limiting middleware (`slowapi`)
3. ~~Add input sanitization on all request fields~~ ✅ Done — `src/utils/prompt_template.py`
4. Refactor `config` global singleton for FastAPI `Depends`
5. Add startup validation for non-localhost `LOCAL_AI_BASE_URL`

Only after all 5 are done: scaffold the FastAPI app and wire endpoints.

## Kanban Rules (`BACKLOG.md`)
- **Todo:** New features and bugs.
- **In Progress:** Only 1-2 tasks at a time to prevent context fragmentation.
- **Done:** Verified, tested, and committed tasks.
