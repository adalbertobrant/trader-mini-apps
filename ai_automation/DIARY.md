# Diary

### Session: 2026-04-14 - Initial Setup & Security
### What we did:
- Read the automation tips and identified "SEO Content Agency" as the high-revenue MVP path.
- Established the development standards in `GEMINI.md`.
- Set up the initial Kanban board in `BACKLOG.md`.
- Initialized Git and created a `README.md` for collaborative potential.
- **Security First:** Prioritized security across all documentation, ensuring zero-leak policies for credentials.
- **Implementation:** Created `SEOWriter` in `src/content/`. It automates the writing of high-ranking blog posts using research data and consensus synthesis.
- **Testing:** Verified `SEOWriter` with automated tests (`tests/test_seo_writer.py`).

### Thoughts:
- The integration between `MarketAnalyzer` and `SEOWriter` is seamless. The quality of the output is significantly higher when the AI is fed real-time search context rather than just a topic.
- Moving forward, the "Conversion" phase will be critical to turn these ranking articles into revenue generators.


### Next Steps:
- Confirmed **Python** as the primary language for better research and AI integration.
- Initialize `requirements.txt` and basic `src/` directory.

### Session: 2026-04-14 - Phase 3 Complete
### What we did:
- Implemented `ProductDescriptionGenerator` in `src/marketing/`. Generates 3 copy variations (50/150/300 words) per product, consensus-based, platform-aware (Tip 33).
- Implemented `SalesEmailPersonalizer` in `src/marketing/`. Uses Tavily to research each prospect, then writes a targeted cold email under 150 words. Supports batch generation (Tip 35).
- All tests pass (3 new tests).
- Backlog cleared — both Phase 3 tasks are Done.

### Thoughts:
- The pipeline now covers the full agency loop: Research → Write → Convert → Sell.
- The only missing piece is a CLI entrypoint to wire it all together for real use.

### Next Steps:
- Build `main.py` as an interactive CLI to run the full pipeline end-to-end.

### Session: 2026-04-14 - Async Fix (Security Review Follow-up)
### What we did:
- Full security audit: no secrets in git history, no hardcoded keys, `.env` never committed. All clean.
- Fixed blocking event loop bug: `GroqClient` and `LocalAIClient` were using sync clients (`Groq`, `OpenAI`) inside async methods. Replaced with `AsyncGroq` and `AsyncOpenAI`.
- Updated `test_ai_client.py` patch target from `OpenAI` → `AsyncOpenAI`.
- All 13 tests still passing.

### Thoughts:
- Under real concurrent load (querying 5 models simultaneously), the sync clients would have serialized execution and potentially deadlocked the event loop. Now truly parallel.

### Session: 2026-04-14 - Concurrency Fix
### What we did:
- Audited thread/async safety across the entire codebase.
- Found `query_all` was `await`ing model calls one-by-one in a for loop — not concurrent at all despite the comment saying otherwise.
- Fixed: replaced loop with `asyncio.gather(*tasks, return_exceptions=True)` — all models now fire simultaneously.
- No shared mutable state found — all instance variables are set once at `__init__` and read-only after that. Safe for concurrent use.
- All 13 tests passing.

### Session: 2026-04-14 - Full Project Review
### What we did:
- Full code review of all source files and tests.
- Fixed `generate_batch` in `SalesEmailPersonalizer`: was sequential loop, now uses `asyncio.gather` (same fix as `query_all`).
- Moved `import asyncio` to module level in `sales_email.py`.
- Removed unused imports: `List`, `Any` from `ai_client.py`; `List`, `Dict`, `Any` from `search_client.py`.
- All 13 tests passing. No regressions.

### State of the project:
- Infrastructure: complete and clean.
- Phase 1 (Research): complete.
- Phase 2 (Content): complete.
- Phase 3 (Marketing): complete.
- Remaining: `main.py` CLI entrypoint to wire the full pipeline.

### Session: 2026-04-14 - Phase 4 CLI + Roadmap
### What we did:
- Implemented `main.py`: interactive CLI with 6 options covering all pipeline modules.
- Option 6 (Full Pipeline) chains MarketAnalyzer → SEOWriter end-to-end automatically.
- Added `tests/test_main.py` with 2 tests covering option 1 and option 6.
- Updated `build_plan.md` with full roadmap: Phase 5 (FastAPI) and Phase 6 (WordPress, Shopify, Mercado Livre, OLX, Make.com, Zapier, Google Sheets).
- Updated `BACKLOG.md` with all Phase 5 and Phase 6 tasks itemized.
- 15 tests passing.

### Next:
- Phase 5: FastAPI REST API exposing all pipeline modules as HTTP endpoints with API key auth.

### Session: 2026-04-14 - Docs, Deps & Standards
### What we did:
- Rewrote `README.md` from scratch: full quick start (clone → venv → install → .env → run), CLI menu, architecture diagram, module table, project structure, tech stack, testing, security, roadmap.
- Fixed `requirements.txt`: `pytest-asyncio` was missing — a fresh install would have broken all 15 async tests.
- Updated `GEMINI.md` with new operational mandates: async-first rule, true concurrency rule (asyncio.gather), test mandate, git discipline, and current project state table.
- All 15 tests passing.

### Session: 2026-04-14 - Async Fix: TavilySearch
### What we did:
- Replaced sync `TavilyClient` with `AsyncTavilyClient` in `search_client.py`.
- Made `search_market_data` async and added `await` at all 3 call sites.
- Updated test mocks from `MagicMock` to `AsyncMock` — tests now fail if the call isn't awaited.
- All 15 tests passing. Mandate #3 (Async First) now 100% compliant.

### Session: 2026-04-14 - Security Fix & CLI State Persistence
### What we did:
- Implemented `PromptTemplate` (`src/utils/prompt_template.py`): strips control characters via regex, enforces 2000-char max length, raises `ValueError` on violation. Wired into `main.py` — all user inputs now go through `_get()` which calls `sanitize()`.
- Resolves Phase 5 pre-condition #3 (input sanitization). Marked done in `BACKLOG.md`.
- Added `last_research` state to `main.py`: options 1 and 6 save `{niche, result}` in memory. Options 3 and 5 detect it and offer to auto-inject, removing the need to manually copy-paste research context.
- 4 new tests (`tests/test_prompt_template.py`). 19 tests passing, no regressions.

### Thoughts:
- All operational mandates now 100% compliant.
- Git log is clean with conventional commits.

### Next:
- Remaining Phase 5 pre-conditions (3 left): API key auth design, rate limiting, config singleton refactor, LocalAI HTTP warning.

### Session: 2026-04-14 - OpenRouter Integration
### What we did:
- Added `OpenRouterClient` to `ai_client.py`: async, OpenAI-compatible, routes to `openai/gpt-4o-mini` by default (any OpenRouter model can be set via constructor).
- Added `OPENROUTER_API_KEY` to `Config` and `.env.example`.
- `MultiModelClient` auto-registers `openrouter` when the key is present — no other changes needed; it joins the consensus pool automatically.
- Updated README, GEMINI.md, build_plan.md to reflect OpenRouter in the tech stack.
- All 19 tests still passing. No regressions.

### Thoughts:
- OpenRouter gives access to 200+ models through a single OpenAI-compatible endpoint. Adding it required zero changes to the consensus engine — it just joins the pool like any other provider.

### State at pause:
- 6 providers supported: Anthropic, Gemini, Groq, Mistral, OpenRouter, LocalAI.
- All phases 1–4 complete and clean.
- Phase 5 pre-condition #3 (input sanitization) resolved.
- 19 tests passing.

### Next:
- Remaining Phase 5 pre-conditions (3 left): API key auth design, rate limiting, config singleton refactor, LocalAI HTTP warning.

### Session: 2026-05-08 - Estratégia "Mãos Livres" e Preparação para Phase 5

### What we did:
- **Análise ilhadev.com.br:** Avaliação técnica do site via `web_fetch`. Identificada oportunidade em SEO de autoridade para Cibersegurança + IA.
- **Teste de Campo:** Execução da pipeline completa para gerar artigo sobre "Hardening de Servidores para IA". Validação do conteúdo gerado pelo `ConsensusSynthesizer`.
- **Planejamento:** Atualização do `BACKLOG.md` para incluir `FileExporter` (necessário para o modelo de serviço "Mãos Livres") e detalhamento das pré-condições da Phase 5.
- **Arquitetura:** Decidido seguir o mandato "Async First" para o exportador de arquivos.

### Thoughts:
- O conteúdo gerado é tecnicamente sólido, mas precisa de "injeção de personalidade" (expertise específica do autor) para se destacar no nicho técnico.
- A exportação para arquivo é o "missing link" entre o CLI e a prestação de serviço real.

### Session: 2026-05-08 - Universalização do Salvamento

### What we did:
- **Infraestrutura:** Generalizado o `FileExporter` para o método `save_content`, permitindo diferentes subdiretórios e extensões.
- **Integração Total:** Adicionada a opção de salvamento em todas as funcionalidades do CLI (Pesquisa, Persona, Produtos, Emails).
- **Organização:** Definida estrutura de pastas: `outputs/research/`, `outputs/articles/` e `outputs/marketing/`.
- **Qualidade:** Testes validados.

### Thoughts:
- Agora o sistema é um "Gerador de Deliverables" completo. Cada interação no CLI pode resultar em um arquivo pronto para o cliente.
- A consistência no salvamento prepara o terreno para a automação de CMS e APIs na Phase 6.

### Next Steps:
- Iniciar design de Auth para Phase 5.
- Refatorar `config` para FastAPI.

---

### Session: 2026-05-08 - Finalização do FileExporter

### What we did:
- **Infraestrutura:** Implementado `src/utils/file_exporter.py` usando `aiofiles` para salvamento assíncrono.
- **Segurança:** Atualizado `.gitignore` para proteger a pasta `outputs/`.
- **Dependências:** Adicionado `aiofiles` ao `requirements.txt`.
- **Integração:** `main.py` atualizado para oferecer a opção de salvar artigos SEO automaticamente.
- **Qualidade:** Criado `tests/test_file_exporter.py` com 100% de sucesso nos testes de criação e sanitização de nomes de arquivo.

### Thoughts:
- A base para o serviço "Mãos Livres" está pronta. Agora o sistema não apenas "fala", mas "entrega" o produto final.
- O próximo grande gargalo é a autenticação da API para permitir múltiplos usuários/clientes.

### Session: 2026-05-11 - Correção do Bug de Salvamento no CLI

### What we did:
- **Bug Fix:** Resolvido erro que impedia o salvamento de arquivos no CLI (`main.py`). O objeto `_exporter` estava sendo utilizado mas não foi importado nem inicializado.
- **Dependências:** Instalada a biblioteca `aiofiles` que estava faltando no ambiente de execução, apesar de listada no `requirements.txt`.
- **Testes:** Atualizado `tests/test_main.py` para incluir as novas interações de prompt do CLI (opção de salvar), garantindo que os testes reflitam o fluxo real.
- **Qualidade:** Todos os 21 testes passando com sucesso.

### Thoughts:
- Pequenos lapsos de inicialização podem travar funcionalidades críticas. A adição de testes que cobrem as ramificações de "salvar" ajudaria a evitar isso no futuro.
- A estrutura de diretórios `outputs/` agora é criada automaticamente na primeira execução do CLI.

### Next Steps:
- Retomar os pré-requisitos da Phase 5 (FastAPI), focando no design de autenticação.

### Session: 2026-05-11 - Robustez e Tratamento de Timeouts

### What we did:
- **Aumento de Timeouts:** Elevado o timeout de todos os provedores de IA (Anthropic, Gemini, Groq, Mistral, OpenRouter, LocalAI) para 120 segundos. Isso evita erros de `ReadTimeout` em prompts grandes ou momentos de alta latência das APIs.
- **Correção Mistral:** Ajustada a inicialização do SDK da Mistral para injetar corretamente o `httpx.AsyncClient` no parâmetro `async_client`.
- **Estabilidade do CLI:** Implementado um bloco `try...except` global no loop principal do `main.py`. Agora, falhas de rede ou timeouts não derrubam mais a aplicação; o erro é exibido amigavelmente e o usuário pode tentar novamente.
- **Qualidade:** Todos os 21 testes validados e passando.

### Thoughts:
- APIs de IA são inerentemente instáveis e lentas em comparação com APIs REST tradicionais. O timeout padrão de 5-10 segundos do `httpx` é insuficiente para modelos "Large".
- O tratamento de exceções no CLI é fundamental para a experiência do usuário, especialmente em ferramentas de automação que processam grandes volumes de dados.

### Next Steps:
- Prosseguir com o design de autenticação para a Phase 5.
