# Build Plan: AI-Driven Content & SEO Agency

## 1. Objective
Build an automated pipeline that generates high-ranking SEO articles and optimized product descriptions for online sale or affiliate marketing.

## 2. Tech Stack
- **Core LLMs:** Anthropic Claude, Google Gemini, Groq (LLaMA), Mistral, OpenRouter, LocalAI (Ollama)
- **Consensus Engine:** Multi-model synthesis for all critical decisions
- **Research Tool:** Tavily API (real-time SERP analysis)
- **CLI:** Python `asyncio` + stdlib
- **API (Phase 5):** FastAPI + Uvicorn
- **Integrations (Phase 6):** WordPress, Shopify, Mercado Livre, OLX, Make.com, Zapier

## 3. Implementation Phases

### ✅ Phase 1: Research Engine
- `MarketAnalyzer`: niche analysis + audience insights (Tips 13 & 19)
- Tavily integration for real-time SERP context

### ✅ Phase 2: Content Engine
- `SEOWriter`: consensus-based SEO article generation + meta data (Tip 05)

### ✅ Phase 3: Conversion & Sales
- `ProductDescriptionGenerator`: 3-variation benefit-led copy (Tip 33)
- `SalesEmailPersonalizer`: Tavily-powered prospect research + cold email batch (Tip 35)

### ✅ Phase 4 (CLI): Command-Line Interface
- `main.py`: interactive CLI wiring the full Research → Content → Convert → Sell pipeline

### 🔜 Phase 5: REST API (FastAPI)
- Expose all pipeline modules as HTTP endpoints
- Async endpoints using `asyncio` (non-blocking, production-ready)
- Planned endpoints:
  - `POST /research/niche` — MarketAnalyzer.analyze_niche
  - `POST /research/audience` — MarketAnalyzer.get_audience_insights
  - `POST /content/article` — SEOWriter.write_article
  - `POST /content/meta` — SEOWriter.generate_seo_meta
  - `POST /marketing/product-description` — ProductDescriptionGenerator.generate
  - `POST /marketing/sales-email` — SalesEmailPersonalizer.generate_email
  - `POST /marketing/sales-email/batch` — SalesEmailPersonalizer.generate_batch
- Auth: API key header (`X-API-Key`)
- Stack: FastAPI + Uvicorn + Pydantic request/response models

#### ⛔ Pre-conditions (must be resolved before Phase 5 starts)

1. **API key auth design:** Decide where the `X-API-Key` lives (env var), how it is rotated, and whether IP allowlisting or scoped keys are needed. A single static key with no rotation strategy is insufficient for production.

2. **Rate limiting:** Each request fans out to 5 AI providers simultaneously. A runaway or malicious request can burn API credits instantly. Rate limiting middleware (e.g. `slowapi`) must be in place before any endpoint is exposed.

3. **Input sanitization:** User input currently goes directly into LLM prompts with no length limits or content validation. Prompt injection via API requests is a known LLM attack vector. All request fields must be validated (max length, stripped of control characters) before being passed to the pipeline.

4. **Config singleton refactor:** `config = Config()` is instantiated at module import time. This is fragile when the API server forks workers or when env vars need to change at runtime. Evaluate dependency injection (e.g. FastAPI `Depends`) instead of the global singleton.

5. **LocalAI HTTP warning:** `LOCAL_AI_BASE_URL` defaults to `http://` (unencrypted). If pointed at a remote host instead of localhost, all LLM traffic is exposed. Add a startup validation that warns or rejects non-localhost HTTP URLs.

### 🔜 Phase 6: CMS & Platform Integrations
- **WordPress:** REST API (`/wp-json/wp/v2/posts`) — auto-publish SEO articles as drafts
- **Shopify:** Admin API — push product descriptions directly to product listings
- **Mercado Livre:** Listing API — generate and publish product ads
- **OLX:** Listing API — generate and publish classified ads
- **Make.com / Zapier:** Webhook triggers — connect pipeline to any no-code workflow
- **Google Sheets:** Export research reports and content calendars

## 4. Quality Control
- Consensus engine (3+ models) for all critical outputs
- Fact-checking via Tavily real-time search context
- Human-in-the-loop: review before publishing (until Phase 6 auto-publish is validated)
