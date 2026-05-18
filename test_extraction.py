"""
Test Knowledge Extraction Engine
Tests Gemini-powered knowledge extraction on demo data
"""

import json
import logging
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config import settings
from processing.knowledge_extractor import KnowledgeExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


def test_slack_extraction():
    """Test extraction from Slack messages"""
    console.print("\n[bold cyan]Testing Slack Message Extraction[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo Slack messages
    with open('demo/data/slack_messages.json') as f:
        messages = json.load(f)
    
    # Find the PostgreSQL failure message
    failure_msg = next(
        (m for m in messages if 'PostgreSQL migration' in m['text'] and 'failed' in m['text'].lower()),
        None
    )
    
    if not failure_msg:
        console.print("[red]Could not find PostgreSQL failure message[/red]")
        return
    
    console.print(f"\n[yellow]Input Message:[/yellow]")
    console.print(f"Channel: {failure_msg['channel']}")
    console.print(f"User: {failure_msg['username']}")
    console.print(f"Text: {failure_msg['text'][:200]}...")
    
    # Extract knowledge
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    
    console.print("\n[yellow]Calling Gemini API...[/yellow]")
    knowledge_items = extractor.extract_knowledge(
        text=failure_msg['text'],
        source_type='slack',
        source_id=failure_msg['id']
    )
    
    # Display results
    console.print(f"\n[green]✓ Extracted {len(knowledge_items)} knowledge items[/green]\n")
    
    for idx, item in enumerate(knowledge_items, 1):
        panel_content = f"""[bold]Title:[/bold] {item.title}
[bold]Type:[/bold] {item.content_type}
[bold]Outcome:[/bold] {item.outcome}
[bold]Importance:[/bold] {item.importance_score}/10

[bold]Summary:[/bold]
{item.summary}

[bold]Key Facts:[/bold]
{chr(10).join(f'  • {fact}' for fact in item.key_facts)}

[bold]People:[/bold] {', '.join(item.people_involved)}
[bold]Topics:[/bold] {', '.join(item.topics)}
[bold]Date:[/bold] {item.date_occurred or 'Unknown'}
"""
        console.print(Panel(panel_content, title=f"[bold]Knowledge Item {idx}[/bold]", border_style="cyan"))


def test_jira_extraction():
    """Test extraction from Jira ticket"""
    console.print("\n\n[bold cyan]Testing Jira Ticket Extraction[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo Jira tickets
    with open('demo/data/jira_tickets.json') as f:
        tickets = json.load(f)
    
    # Find the PostgreSQL migration ticket
    ticket = next((t for t in tickets if t['id'] == 'ENG-1234'), None)
    
    if not ticket:
        console.print("[red]Could not find ENG-1234 ticket[/red]")
        return
    
    console.print(f"\n[yellow]Input Ticket:[/yellow]")
    console.print(f"ID: {ticket['id']}")
    console.print(f"Title: {ticket['title']}")
    console.print(f"Status: {ticket['status']} - {ticket['resolution']}")
    
    # Combine ticket data
    ticket_text = f"""
Title: {ticket['title']}
Description: {ticket['description']}
Status: {ticket['status']}
Resolution: {ticket['resolution']}
Priority: {ticket['priority']}
Assignee: {ticket['assignee']}

Comments:
{chr(10).join(f"- {c['author']}: {c['text']}" for c in ticket['comments'])}
"""
    
    # Extract knowledge
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    
    console.print("\n[yellow]Calling Gemini API...[/yellow]")
    knowledge_items = extractor.extract_knowledge(
        text=ticket_text,
        source_type='jira',
        source_id=ticket['id']
    )
    
    # Display results
    console.print(f"\n[green]✓ Extracted {len(knowledge_items)} knowledge items[/green]\n")
    
    for idx, item in enumerate(knowledge_items, 1):
        panel_content = f"""[bold]Title:[/bold] {item.title}
[bold]Type:[/bold] {item.content_type}
[bold]Outcome:[/bold] {item.outcome}
[bold]Importance:[/bold] {item.importance_score}/10

[bold]Summary:[/bold]
{item.summary}

[bold]Key Facts:[/bold]
{chr(10).join(f'  • {fact}' for fact in item.key_facts)}

[bold]People:[/bold] {', '.join(item.people_involved)}
[bold]Topics:[/bold] {', '.join(item.topics)}
"""
        console.print(Panel(panel_content, title=f"[bold]Knowledge Item {idx}[/bold]", border_style="green"))


def test_document_extraction():
    """Test extraction from document"""
    console.print("\n\n[bold cyan]Testing Document Extraction[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo documents
    with open('demo/data/documents.json') as f:
        documents = json.load(f)
    
    # Find the React ADR
    doc = next((d for d in documents if d['id'] == 'ADR-015'), None)
    
    if not doc:
        console.print("[red]Could not find ADR-015 document[/red]")
        return
    
    console.print(f"\n[yellow]Input Document:[/yellow]")
    console.print(f"ID: {doc['id']}")
    console.print(f"Title: {doc['title']}")
    console.print(f"Type: {doc['type']}")
    
    # Extract knowledge
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    
    console.print("\n[yellow]Calling Gemini API...[/yellow]")
    knowledge_items = extractor.extract_knowledge(
        text=doc['content'],
        source_type='document',
        source_id=doc['id']
    )
    
    # Display results
    console.print(f"\n[green]✓ Extracted {len(knowledge_items)} knowledge items[/green]\n")
    
    for idx, item in enumerate(knowledge_items, 1):
        panel_content = f"""[bold]Title:[/bold] {item.title}
[bold]Type:[/bold] {item.content_type}
[bold]Outcome:[/bold] {item.outcome}
[bold]Importance:[/bold] {item.importance_score}/10

[bold]Summary:[/bold]
{item.summary}

[bold]Key Facts:[/bold]
{chr(10).join(f'  • {fact}' for fact in item.key_facts)}

[bold]People:[/bold] {', '.join(item.people_involved)}
[bold]Topics:[/bold] {', '.join(item.topics)}
"""
        console.print(Panel(panel_content, title=f"[bold]Knowledge Item {idx}[/bold]", border_style="blue"))


def main():
    """Run all tests"""
    console.print("\n[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]   Knowledge Extraction Engine - Test Suite[/bold magenta]")
    console.print("[bold magenta]   Powered by Google Gemini 1.5 Pro[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]")
    
    try:
        # Test 1: Slack extraction
        test_slack_extraction()
        
        # Test 2: Jira extraction
        test_jira_extraction()
        
        # Test 3: Document extraction
        test_document_extraction()
        
        # Summary
        console.print("\n\n[bold green]✅ All extraction tests complete![/bold green]")
        console.print("[dim]Knowledge extraction engine is working correctly with Gemini 1.5 Pro[/dim]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]\n")
        raise


if __name__ == "__main__":
    main()
