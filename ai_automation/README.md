# 🚀 AI-Driven SEO & Content Agency Engine

Automates the full lifecycle of a digital content agency — from market research to SEO article generation, product descriptions, and personalized sales outreach.

Built for niche site owners, affiliate marketers, and e-commerce brands who need high-quality, high-ranking content at scale.

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/adalbertobrant/trader-mini-apps.git
cd ai_automation
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:
```env
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
MISTRAL_API_KEY=your_mistral_key
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key

# Optional: local Ollama instance
LOCAL_AI_BASE_URL=http://localhost:8080/v1
LOCAL_AI_MODEL=llama3
```

> You need **at least one** AI API key to run the pipeline. The system is resilient — it only initializes clients for keys that are present, and the consensus engine works with however many models respond. With a single key, that one model handles both generation and synthesis. With more keys, quality improves through cross-model validation.
>
> If no cloud keys are set, the system falls back to LocalAI (Ollama). If Ollama is also not running, the pipeline will return a graceful error rather than crash.

### 5. Run the CLI
```bash
python main.py
```

You'll see an interactive menu:
```
Select a task:
  1. Market Research (niche analysis)
  2. Audience Insights
  3. Write SEO Article
  4. Generate Product Descriptions
  5. Generate Sales Email(s)
  6. Full Pipeline (Research -> Article)
  0. Exit
```

---

## 🏗️ Architecture

The pipeline has four stages, each consensus-based (3+ AI models synthesized into one output):

```
Tavily Search (real-time SERP)
        ↓
MarketAnalyzer  →  SEOWriter  →  ProductDescriptionGenerator
                                         ↓
                              SalesEmailPersonalizer
```

| Module | File | Tips |
|---|---|---|
| Market Research | `src/research/market_analyzer.py` | 13, 19 |
| SEO Article Writer | `src/content/seo_writer.py` | 05 |
| Product Descriptions | `src/marketing/product_description.py` | 33 |
| Sales Email Personalizer | `src/marketing/sales_email.py` | 35 |
| Multi-Model Client | `src/utils/ai_client.py` | — |
| Consensus Synthesizer | `src/utils/consensus.py` | — |
| Prompt Sanitizer | `src/utils/prompt_template.py` | — |
| Config (secure) | `src/utils/config.py` | — |

---

## 📁 Project Structure

```
ai_automation/
├── main.py                        # CLI entrypoint
├── src/
│   ├── research/
│   │   └── market_analyzer.py     # Niche research + audience insights
│   ├── content/
│   │   └── seo_writer.py          # SEO article + meta generation
│   ├── marketing/
│   │   ├── product_description.py # Product copy (3 variations)
│   │   └── sales_email.py         # Cold email personalizer
│   └── utils/
│       ├── ai_client.py           # Multi-model async client
│       ├── consensus.py           # Synthesis engine
│       ├── search_client.py       # Tavily async wrapper
│       └── config.py              # Secure config (pydantic-settings)
├── tests/                         # Full test suite (pytest)
├── .env.example                   # API key template
├── requirements.txt
├── GEMINI.md                      # Dev standards & operational mandates
├── BACKLOG.md                     # Kanban task tracking
├── HISTORY.md                     # Architecture decisions & milestones
├── DIARY.md                       # Session logs
└── build_plan.md                  # Full technical roadmap
```

---

## 🛠️ Tech Stack

- **Python** 3.10+
- **AI Models:** Anthropic Claude, Google Gemini, Groq (LLaMA), Mistral, OpenRouter, LocalAI (Ollama)
- **Search:** Tavily API (real-time SERP, async)
- **Config:** pydantic-settings (secure, `.env`-based)
- **Tests:** pytest + pytest-mock + pytest-asyncio

---

## 🧪 Running Tests

```bash
python -m pytest
```

All modules have full test coverage. Tests use mocks — no real API calls are made.

---

## 🔒 Security

- Never commit `.env`. It is git-ignored.
- All API keys are loaded via `pydantic-settings` — never hardcoded.
- Zero-leak policy: no keys in logs, code, or version control.

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| 1 — Research Engine | ✅ Done | MarketAnalyzer + Tavily |
| 2 — Content Engine | ✅ Done | SEOWriter |
| 3 — Conversion & Sales | ✅ Done | ProductDescriptionGenerator + SalesEmailPersonalizer |
| 4 — CLI | ✅ Done | `main.py` interactive pipeline |
| 5 — REST API | 🔜 Next | FastAPI + Uvicorn + API key auth |
| 6 — Integrations | 🔜 Planned | WordPress, Shopify, Mercado Livre, OLX, Make.com, Zapier, Google Sheets |

See `build_plan.md` for full technical details on upcoming phases.

---

## 🤝 Contributing

1. Check `BACKLOG.md` for open tasks.
2. Read `GEMINI.md` for development standards (security, consensus rules, Kanban).
3. All PRs must include tests and pass the full test suite.
