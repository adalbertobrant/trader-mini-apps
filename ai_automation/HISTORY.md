# History

## [2026-04-14] — Project Kickoff & Infrastructure
- Initialized Git repository and Python environment (`requirements.txt`, `src/` structure).
- Established "Security First" as a core mandate in `GEMINI.md`.
- Implemented `Config` class via `pydantic-settings` for secure `.env`-based key loading.
- Added `.gitignore` to prevent committing `.env` and secrets.
- Created core documentation: `GEMINI.md`, `build_plan.md`, `marketing.md`, `BACKLOG.md`.

## [2026-04-14] — Multi-Model Consensus Architecture
- **Architectural Pivot:** Shifted from single-model (Claude) to a Multi-Model Consensus Engine (Anthropic, Gemini, Groq, Mistral, LocalAI) to maximize output quality through cross-validation.
- Implemented `MultiModelClient` — async wrapper for all 5 providers.
- Implemented `ConsensusSynthesizer` — merges model outputs into a single "Gold Standard" result.
- Integrated Tavily Search API for real-time SERP context.

## [2026-04-14] — Phase 1: Research Engine
- Implemented `MarketAnalyzer`: niche analysis (Tip 13) + audience insights (Tip 19).
- Tavily search context injected into every research prompt.

## [2026-04-14] — Phase 2: Content Engine
- Implemented `SEOWriter`: consensus-based SEO article generation + meta data (Tip 05).

## [2026-04-14] — Phase 3: Conversion & Sales
- Implemented `ProductDescriptionGenerator`: 3-variation benefit-led copy for any platform (Tip 33).
- Implemented `SalesEmailPersonalizer`: Tavily-powered prospect research + cold email batch (Tip 35).

## [2026-04-14] — Async & Concurrency Fixes
- `GroqClient` and `LocalAIClient`: replaced sync `Groq`/`OpenAI` with `AsyncGroq`/`AsyncOpenAI`.
- `query_all`: replaced sequential `await` loop with `asyncio.gather` — all models now fire in parallel.
- `generate_batch` in `SalesEmailPersonalizer`: same fix applied.
- Concurrency model and thread-safety caveat documented in `query_all` docstring.

## [2026-04-14] — Phase 4: CLI
- Implemented `main.py`: interactive CLI with 6 options covering the full Research → Content → Convert → Sell pipeline.
- Option 6 auto-chains `MarketAnalyzer` → `SEOWriter` end-to-end.

## [2026-04-14] — Docs, Deps & Standards
- Rewrote `README.md`: full quick start, CLI menu, architecture, project structure, roadmap.
- Fixed `requirements.txt`: added missing `pytest-asyncio` (was installed but not declared).
- Updated `GEMINI.md`: added async-first, concurrency, test, and git discipline mandates; added project state table.
- Cleaned unused imports (`List`, `Any`, `Dict`) from `ai_client.py` and `search_client.py`.

## [2026-04-14] — OpenRouter Integration
- Added `OpenRouterClient` to `src/utils/ai_client.py`: OpenAI-compatible async client pointing at `https://openrouter.ai/api/v1`. Default model: `openai/gpt-4o-mini` (configurable).
- Added `OPENROUTER_API_KEY` to `Config` in `src/utils/config.py` and `.env.example`.
- `MultiModelClient._initialize_clients` now registers `openrouter` when the key is present — participates in consensus automatically.
- Updated README, GEMINI.md, build_plan.md tech stack references to include OpenRouter.

- Implemented `PromptTemplate` in `src/utils/prompt_template.py`: strips control characters (prompt injection mitigation) and enforces a 2000-char max length on all user inputs. Wired into `main.py` via `_get()` helper — every user-facing `input()` call now goes through sanitization.
- Resolves BACKLOG pre-condition #3 for Phase 5 (input sanitization on all request fields).
- Added state persistence to `main.py`: `last_research` dict holds the last niche + result from options 1 and 6. Options 3 (SEO Article) and 5 (Sales Email) detect saved research and offer to auto-inject it, eliminating manual copy-paste between tasks.
- 4 new tests in `tests/test_prompt_template.py`. 19 tests passing total.
