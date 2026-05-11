# Backlog

## Todo

### Phase 5: REST API (FastAPI)
#### Infrastructure Enhancements
- [ ] Implement `FileExporter` utility to save outputs (MD, JSON) to `outputs/` directory
- [ ] Add `outputs/` to `.gitignore`

#### Pre-conditions (security — must be resolved first)
- [ ] Design API key auth strategy: storage, rotation, scoping (not just a static env var)
- [ ] Add rate limiting middleware (`slowapi` or equivalent) — each request fans out to 5 AI providers
- [x] Add input sanitization on all request fields (max length, strip control chars) — prompt injection risk ✅ Done
- [ ] Refactor `config` global singleton — evaluate FastAPI `Depends` for worker-safe config injection
- [ ] Add startup validation: warn/reject non-localhost `LOCAL_AI_BASE_URL` over HTTP

#### Endpoints
- [ ] Set up FastAPI app skeleton with Uvicorn and API key auth middleware
- [ ] `POST /research/niche` — MarketAnalyzer.analyze_niche
- [ ] `POST /research/audience` — MarketAnalyzer.get_audience_insights
- [ ] `POST /content/article` — SEOWriter.write_article
- [ ] `POST /content/meta` — SEOWriter.generate_seo_meta
- [ ] `POST /marketing/product-description` — ProductDescriptionGenerator.generate
- [ ] `POST /marketing/sales-email` — SalesEmailPersonalizer.generate_email
- [ ] `POST /marketing/sales-email/batch` — SalesEmailPersonalizer.generate_batch

### Phase 6: CMS & Platform Integrations
- [ ] WordPress REST API integration (auto-publish articles as drafts)
- [ ] Shopify Admin API integration (push product descriptions)
- [ ] Mercado Livre Listing API integration
- [ ] OLX Listing API integration
- [ ] Make.com / Zapier webhook support
- [ ] Google Sheets export (research reports, content calendars)

## In Progress
- [ ] Design API key auth strategy (Phase 5 Pre-condition)
## Done
- [x] Initial strategy extraction from `automation_tips.txt`.
- [x] Creation of `build_plan.md` and `marketing.md`.
- [x] Git repository initialization.
- [x] Creation of `README.md` for project documentation and community help.
- [x] **Infrastructure:** Initialize Python environment (requirements.txt, project structure).
- [x] **Security:** Implement `Config` class using `pydantic-settings` for secure key handling.
- [x] **Security:** Verify `Config` class with automated tests (`tests/test_config.py`).
- [x] **Security:** Add `.gitignore` to prevent committing sensitive files.
- [x] **Infrastructure:** Implement Multi-Model Wrapper (Anthropic, Gemini, Groq, Mistral, LocalAI).
- [x] **Core Logic:** Design and implement Consensus Engine (Synthesizer).
- [x] **Phase 1 (Research):** Implement Market Analyzer (Consensus-based).
- [x] **Phase 1 (Research):** Integrate Tavily API for SERP analysis.
- [x] **Phase 2 (Content):** Implement Master SEO Writer (Consensus-based).
- [x] **Phase 3 (Conversion):** Implement Product Description Generator (Consensus-based).
- [x] **Phase 3 (Marketing):** Implement Sales Email Personalizer (Tip 35).
- [x] **fix(async):** Replace sync Groq/OpenAI clients with AsyncGroq/AsyncOpenAI.
- [x] **fix(concurrency):** Use asyncio.gather in query_all and generate_batch for true parallel execution.
- [x] **Phase 4 (CLI):** Implement main.py interactive CLI for the full pipeline.
- [x] **docs:** Rewrite README.md with full setup, usage, architecture, and roadmap.
- [x] **fix(deps):** Add missing pytest-asyncio to requirements.txt.
- [x] **Security (Phase 5 pre-condition):** Add input sanitization on all request fields — `src/utils/prompt_template.py`, wired into `main.py` via `_get()`.
- [x] **feat(providers):** Add OpenRouterClient to `ai_client.py` + `OPENROUTER_API_KEY` to config and `.env.example`.
- [x] **feat(cli):** Add state persistence to `main.py` — last niche research auto-injected into tasks 3 & 5.
