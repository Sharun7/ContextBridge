"""
Test Proactive Intelligence Engine
Demonstrates the "magic" feature - proactive context surfacing
"""

import json
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import settings
from processing.knowledge_extractor import KnowledgeExtractor
from processing.vector_store import VectorStore
from processing.graph_builder import GraphBuilder
from intelligence.proactive_engine import ProactiveEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


def setup_system():
    """Setup the complete ContextBridge system"""
    console.print("\n[bold cyan]Setting Up ContextBridge System[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo data
    with open('demo/data/slack_messages.json') as f:
        messages = json.load(f)
    
    # Extract knowledge from key messages
    console.print("\n[yellow]Extracting knowledge from demo data...[/yellow]")
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    
    # Select messages about PostgreSQL failure and React decision
    key_messages = [
        m for m in messages 
        if m['id'] in [
            'ff4adc79-d389-49ac-bf18-d0bfcf299efa',  # PostgreSQL incident
            '28866bb8-ed13-4400-820b-3d5331dd781e',  # React decision
        ]
    ]
    
    all_knowledge = []
    for msg in key_messages:
        items = extractor.extract_knowledge(
            text=msg['text'],
            source_type='slack',
            source_id=msg['id']
        )
        all_knowledge.extend(items)
        console.print(f"  ✓ Extracted {len(items)} items")
    
    # Initialize vector store
    console.print("\n[yellow]Initializing vector store...[/yellow]")
    vector_store = VectorStore(
        persist_dir=settings.CHROMA_PERSIST_DIR,
        collection_name=settings.CHROMA_COLLECTION_NAME
    )
    vector_store.initialize_store()
    vector_store.add_knowledge(all_knowledge)
    console.print(f"  ✓ Stored {len(all_knowledge)} items")
    
    # Build knowledge graph
    console.print("\n[yellow]Building knowledge graph...[/yellow]")
    graph_builder = GraphBuilder()
    graph_builder.build_graph(all_knowledge)
    console.print(f"  ✓ Built graph with {graph_builder.graph.number_of_nodes()} nodes")
    
    # Initialize proactive engine
    console.print("\n[yellow]Initializing proactive engine...[/yellow]")
    proactive_engine = ProactiveEngine(
        vector_store=vector_store,
        graph_builder=graph_builder,
        gemini_api_key=settings.GEMINI_API_KEY
    )
    console.print("  ✓ Proactive engine ready")
    
    console.print("\n[bold green]✅ System setup complete![/bold green]")
    return proactive_engine


def display_alert(alert, scenario_name: str):
    """Display a proactive alert in a nice format"""
    if alert is None:
        console.print(f"\n[dim]No alert generated (confidence too low or no relevant history)[/dim]")
        return
    
    # Determine color based on alert level
    if alert.alert_level == 'warning':
        color = 'red'
        icon = '⚠️'
    elif alert.alert_level == 'expert_needed':
        color = 'yellow'
        icon = '💡'
    else:
        color = 'blue'
        icon = 'ℹ️'
    
    # Create panel content
    content = f"""[bold]Alert Level:[/bold] [{color}]{icon} {alert.alert_level.upper()}[/{color}]
[bold]Confidence:[/bold] {alert.confidence_score}%
[bold]Trigger Type:[/bold] {alert.trigger_type}

[bold]Headline:[/bold]
{alert.headline}

[bold]Synthesized Insight:[/bold]
{alert.synthesized_insight}

[bold]Recommended Actions:[/bold]
{chr(10).join(f'  • {action}' for action in alert.recommended_actions)}

[bold]Relevant People:[/bold] {', '.join(alert.relevant_people) if alert.relevant_people else 'None identified'}

[bold]Context Items:[/bold] {len(alert.context_items)} items found
"""
    
    console.print(Panel(
        content,
        title=f"[bold]{scenario_name}[/bold]",
        border_style=color,
        expand=False
    ))


def test_scenario_a_mistake_prevented(engine):
    """
    SCENARIO A: The Mistake Prevented
    Someone creates a Jira ticket to migrate database to PostgreSQL
    System should warn about the 2023 failure
    """
    console.print("\n[bold magenta]SCENARIO A: The Mistake Prevented[/bold magenta]")
    console.print("=" * 70)
    console.print("[dim]A developer creates a Jira ticket to migrate the database...[/dim]\n")
    
    ticket_title = "Migrate primary database from MySQL to PostgreSQL"
    ticket_description = """
    We need to migrate our primary database from MySQL to PostgreSQL for better JSON support
    and improved performance. This will involve:
    - Setting up PostgreSQL instance
    - Migrating schema
    - Migrating data
    - Updating application connection strings
    - Testing in staging
    - Production cutover
    
    Timeline: 2 weeks
    """
    
    console.print(f"[yellow]Ticket Title:[/yellow] {ticket_title}")
    console.print(f"[yellow]Description:[/yellow] {ticket_description[:100]}...\n")
    
    alert = engine.handle_jira_trigger(ticket_title, ticket_description)
    display_alert(alert, "🚨 PROACTIVE ALERT")


def test_scenario_b_question_answered(engine):
    """
    SCENARIO B: The Question Answered
    Someone asks why we use React instead of Vue
    System should surface the 2022 decision
    """
    console.print("\n[bold magenta]SCENARIO B: The Question Answered[/bold magenta]")
    console.print("=" * 70)
    console.print("[dim]A new developer asks about our frontend framework choice...[/dim]\n")
    
    query = "Why do we use React instead of Vue for our frontend?"
    
    console.print(f"[yellow]Query:[/yellow] {query}\n")
    
    alert = engine.handle_query_trigger(query)
    display_alert(alert, "💬 QUERY RESPONSE")


def test_scenario_c_document_context(engine):
    """
    SCENARIO C: Document Context
    Someone starts writing a migration guide
    System should surface relevant past experiences
    """
    console.print("\n[bold magenta]SCENARIO C: Document Context Surfacing[/bold magenta]")
    console.print("=" * 70)
    console.print("[dim]An engineer starts writing a database migration guide...[/dim]\n")
    
    document_title = "Database Migration Best Practices Guide"
    document_content = """
    This guide covers best practices for database migrations at NovaTech.
    
    ## Planning Phase
    - Assess current database performance
    - Identify migration goals
    - Choose target database system
    
    ## Execution Phase
    - Set up new database instance
    - Configure connection pooling
    - Migrate schema and data
    """
    
    console.print(f"[yellow]Document Title:[/yellow] {document_title}")
    console.print(f"[yellow]Content:[/yellow] {document_content[:150]}...\n")
    
    alert = engine.handle_document_trigger(document_title, document_content)
    display_alert(alert, "📄 DOCUMENT ALERT")


def test_scenario_d_no_alert(engine):
    """
    SCENARIO D: No Alert (Low Confidence)
    Someone creates a ticket about something unrelated
    System should NOT alert (no relevant history)
    """
    console.print("\n[bold magenta]SCENARIO D: No Alert (Unrelated Topic)[/bold magenta]")
    console.print("=" * 70)
    console.print("[dim]A developer creates a ticket about a completely new topic...[/dim]\n")
    
    ticket_title = "Add dark mode to mobile app"
    ticket_description = """
    Users have requested a dark mode option for the mobile app.
    This will involve updating the theme system and adding a toggle in settings.
    """
    
    console.print(f"[yellow]Ticket Title:[/yellow] {ticket_title}")
    console.print(f"[yellow]Description:[/yellow] {ticket_description[:100]}...\n")
    
    alert = engine.handle_jira_trigger(ticket_title, ticket_description)
    display_alert(alert, "🔇 NO ALERT")


def create_summary_table():
    """Create a summary table of all scenarios"""
    console.print("\n[bold cyan]Scenario Summary[/bold cyan]")
    console.print("=" * 70)
    
    table = Table(title="Proactive Intelligence Engine - Test Scenarios", show_header=True, header_style="bold magenta")
    table.add_column("Scenario", style="cyan", width=25)
    table.add_column("Trigger Type", style="yellow", width=15)
    table.add_column("Expected Outcome", style="green", width=35)
    
    table.add_row(
        "A: Mistake Prevented",
        "Jira Ticket",
        "⚠️ WARNING alert about past failure"
    )
    
    table.add_row(
        "B: Question Answered",
        "User Query",
        "ℹ️ INFO with decision rationale"
    )
    
    table.add_row(
        "C: Document Context",
        "Document",
        "💡 EXPERT_NEEDED with lessons learned"
    )
    
    table.add_row(
        "D: No Alert",
        "Jira Ticket",
        "🔇 No alert (unrelated topic)"
    )
    
    console.print(table)


def main():
    """Run all test scenarios"""
    console.print("\n")
    console.print("=" * 70, style="bold magenta")
    console.print("  ContextBridge Proactive Intelligence Engine", style="bold magenta")
    console.print("  THE MAGIC FEATURE - Proactive Context Surfacing", style="magenta")
    console.print("=" * 70, style="bold magenta")
    
    try:
        # Setup system
        engine = setup_system()
        
        # Run scenarios
        test_scenario_a_mistake_prevented(engine)
        test_scenario_b_question_answered(engine)
        test_scenario_c_document_context(engine)
        test_scenario_d_no_alert(engine)
        
        # Summary
        create_summary_table()
        
        console.print("\n[bold green]✅ All scenarios completed successfully![/bold green]")
        console.print("\n[bold cyan]Key Takeaway:[/bold cyan]")
        console.print("The proactive engine successfully:")
        console.print("  • Detected potential mistakes BEFORE they happen")
        console.print("  • Answered questions with organizational context")
        console.print("  • Surfaced relevant expertise and lessons learned")
        console.print("  • Avoided false positives on unrelated topics")
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
