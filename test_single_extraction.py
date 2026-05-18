"""
Simple single extraction test
Tests one Slack message to verify Gemini extraction works
"""

import json
import logging
from rich.console import Console
from rich.panel import Panel

from config import settings
from processing.knowledge_extractor import KnowledgeExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


def main():
    """Test single extraction"""
    console.print("\n[bold cyan]Testing Single Knowledge Extraction[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo Slack messages
    with open('demo/data/slack_messages.json') as f:
        messages = json.load(f)
    
    # Find the PostgreSQL failure incident message
    failure_msg = next(
        (m for m in messages if m['id'] == 'ff4adc79-d389-49ac-bf18-d0bfcf299efa'),
        None
    )
    
    if not failure_msg:
        console.print("[red]Could not find incident message[/red]")
        return
    
    console.print(f"\n[yellow]Input Message:[/yellow]")
    console.print(f"Channel: {failure_msg['channel']}")
    console.print(f"User: {failure_msg['username']}")
    console.print(f"Text: {failure_msg['text']}")
    console.print()
    
    # Extract knowledge
    console.print("[yellow]Calling Gemini API...[/yellow]\n")
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    
    knowledge_items = extractor.extract_knowledge(
        text=failure_msg['text'],
        source_type='slack',
        source_id=failure_msg['id']
    )
    
    # Display results
    if len(knowledge_items) == 0:
        console.print("[red]No knowledge items extracted[/red]")
        return
    
    console.print(f"\n[bold green]✓ Extracted {len(knowledge_items)} knowledge item(s)[/bold green]\n")
    
    for idx, item in enumerate(knowledge_items, 1):
        panel_content = f"""[bold]Title:[/bold] {item.title}
[bold]Type:[/bold] {item.content_type}
[bold]Outcome:[/bold] {item.outcome}
[bold]Importance:[/bold] {item.importance_score}/10

[bold]Summary:[/bold]
{item.summary}

[bold]Key Facts:[/bold]
{chr(10).join(f'  • {fact}' for fact in item.key_facts)}

[bold]People:[/bold] {', '.join(item.people_involved) if item.people_involved else 'None'}
[bold]Teams:[/bold] {', '.join(item.teams_involved) if item.teams_involved else 'None'}
[bold]Topics:[/bold] {', '.join(item.topics) if item.topics else 'None'}
[bold]Date:[/bold] {item.date_occurred or 'Unknown'}

[bold]Raw Excerpt:[/bold]
{item.raw_excerpt[:200]}...
"""
        console.print(Panel(panel_content, title=f"[bold]Knowledge Item {idx}[/bold]", border_style="green"))
    
    console.print("\n[bold green]✅ Test completed successfully![/bold green]\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()
