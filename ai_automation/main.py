"""
AI-Driven SEO & Content Agency Engine — CLI Entrypoint

Wires the full pipeline:
  Research (MarketAnalyzer) -> Content (SEOWriter) -> Convert (ProductDescriptionGenerator) -> Sell (SalesEmailPersonalizer)

Usage:
    python main.py
"""
import asyncio
from src.utils.ai_client import MultiModelClient
from src.utils.consensus import ConsensusSynthesizer
from src.utils.prompt_template import PromptTemplate
from src.research.market_analyzer import MarketAnalyzer
from src.content.seo_writer import SEOWriter
from src.marketing.product_description import ProductDescriptionGenerator
from src.marketing.sales_email import SalesEmailPersonalizer

_pt = PromptTemplate()


def _get(prompt: str) -> str:
    """Read and sanitize a single user input."""
    return _pt.sanitize(input(prompt).strip())


def print_section(title: str, content: str):
    print(f"\n{'='*60}\n{title}\n{'='*60}\n{content}\n")


async def run_pipeline():
    print("\n🚀 AI-Driven SEO & Content Agency Engine\n")

    multi_client = MultiModelClient()
    synthesizer = ConsensusSynthesizer(multi_client)

    # State: last niche research result, persisted across menu iterations.
    last_research: dict | None = None  # {"niche": str, "result": str}

    menu = """Select a task:
  1. Market Research (niche analysis)
  2. Audience Insights
  3. Write SEO Article
  4. Generate Product Descriptions
  5. Generate Sales Email(s)
  6. Full Pipeline (Research -> Article)
  0. Exit
"""
    while True:
        print(menu)
        if last_research:
            print(f"  💾 Saved research: \"{last_research['niche']}\" (auto-available for tasks 3 & 5)\n")

        choice = input("Choice: ").strip()

        if choice == "0":
            print("Bye.")
            break

        elif choice == "1":
            try:
                niche = _get("Niche: ")
            except ValueError as e:
                print(f"⚠️  {e}")
                continue
            result = await MarketAnalyzer(synthesizer).analyze_niche(niche)
            last_research = {"niche": niche, "result": result}
            print_section(f"Market Research: {niche}", result)
            
            save = input("Save research to file? [y/N]: ").strip().lower()
            if save == 'y':
                path = await _exporter.save_content(f"research_{niche}", result, "research")
                print(f"✅ Saved to: {path}")

        elif choice == "2":
            try:
                niche = _get("Niche: ")
            except ValueError as e:
                print(f"⚠️  {e}")
                continue
            result = await MarketAnalyzer(synthesizer).get_audience_insights(niche)
            print_section(f"Audience Insights: {niche}", result)

            save = input("Save insights to file? [y/N]: ").strip().lower()
            if save == 'y':
                path = await _exporter.save_content(f"audience_{niche}", result, "research")
                print(f"✅ Saved to: {path}")

        elif choice == "3":
            try:
                topic = _get("Topic: ")
            except ValueError as e:
                print(f"⚠️  {e}")
                continue

            if last_research:
                use_saved = input(
                    f"Use saved research for \"{last_research['niche']}\"? [Y/n]: "
                ).strip().lower()
                context = last_research["result"] if use_saved != "n" else (
                    _get("Research context (or press Enter to skip): ") or "No additional context."
                )
            else:
                try:
                    context = _get("Research context (or press Enter to skip): ") or "No additional context."
                except ValueError as e:
                    print(f"⚠️  {e}")
                    continue

            result = await SEOWriter(synthesizer).write_article(topic, context)
            print_section(f"SEO Article: {topic}", result)

            save = input("Save to file? [y/N]: ").strip().lower()
            if save == 'y':
                path = await _exporter.save_content(topic, result, "articles")
                print(f"✅ Saved to: {path}")

        elif choice == "4":
            try:
                name = _get("Product name: ")
                features = _get("Features: ")
                audience = _get("Target audience: ")
                platform = _get("Platform (website/amazon/etsy) [website]: ") or "website"
            except ValueError as e:
                print(f"⚠️  {e}")
                continue
            result = await ProductDescriptionGenerator(synthesizer).generate(name, features, audience, platform)
            print_section(f"Product Descriptions: {name}", result)

            save = input("Save descriptions to file? [y/N]: ").strip().lower()
            if save == 'y':
                path = await _exporter.save_content(f"product_{name}", result, "marketing")
                print(f"✅ Saved to: {path}")

        elif choice == "5":
            try:
                service = _get("Service you're offering: ")
                companies_input = _get("Company name(s), comma-separated: ")
            except ValueError as e:
                print(f"⚠️  {e}")
                continue

            companies = [c.strip() for c in companies_input.split(",")]

            if last_research:
                use_saved = input(
                    f"Inject saved research for \"{last_research['niche']}\" as context? [Y/n]: "
                ).strip().lower()
                if use_saved != "n":
                    service = f"{service}\n\nContext: {last_research['result']}"

            personalizer = SalesEmailPersonalizer(synthesizer)
            if len(companies) == 1:
                result = await personalizer.generate_email(companies[0], service)
                print_section(f"Sales Email: {companies[0]}", result)
                
                save = input("Save email to file? [y/N]: ").strip().lower()
                if save == 'y':
                    path = await _exporter.save_content(f"email_{companies[0]}", result, "marketing")
                    print(f"✅ Saved to: {path}")
            else:
                results = await personalizer.generate_batch(companies, service)
                batch_content = ""
                for company, email in results.items():
                    print_section(f"Sales Email: {company}", email)
                    batch_content += f"--- EMAIL FOR: {company} ---\n{email}\n\n"
                
                save = input("Save all emails to a single file? [y/N]: ").strip().lower()
                if save == 'y':
                    path = await _exporter.save_content(f"email_batch_{len(companies)}", batch_content, "marketing")
                    print(f"✅ Saved to: {path}")

        elif choice == "6":
            try:
                niche = _get("Niche: ")
                topic = _get("Article topic: ")
            except ValueError as e:
                print(f"⚠️  {e}")
                continue

            analyzer = MarketAnalyzer(synthesizer)
            writer = SEOWriter(synthesizer)

            print("\n⏳ Running market research...")
            research = await analyzer.analyze_niche(niche)
            last_research = {"niche": niche, "result": research}
            print_section("Market Research", research)

            print("⏳ Writing SEO article...")
            article = await writer.write_article(topic, research)
            print_section("SEO Article", article)

            save = input("Save article to file? [y/N]: ").strip().lower()
            if save == 'y':
                path = await _exporter.save_markdown(topic, article)
                print(f"✅ Saved to: {path}")

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
