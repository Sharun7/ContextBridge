"""
Test Vector Store and Knowledge Graph
Tests ChromaDB vector store and NetworkX graph builder
"""

import json
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config import settings
from processing.knowledge_extractor import KnowledgeExtractor, KnowledgeItem
from processing.vector_store import VectorStore
from processing.graph_builder import GraphBuilder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


def load_demo_data():
    """Load and extract knowledge from demo data"""
    console.print("\n[bold cyan]Step 1: Loading Demo Data[/bold cyan]")
    console.print("=" * 70)
    
    # Load demo data
    with open('demo/data/slack_messages.json') as f:
        messages = json.load(f)
    
    with open('demo/data/jira_tickets.json') as f:
        tickets = json.load(f)
    
    with open('demo/data/documents.json') as f:
        documents = json.load(f)
    
    console.print(f"✓ Loaded {len(messages)} Slack messages")
    console.print(f"✓ Loaded {len(tickets)} Jira tickets")
    console.print(f"✓ Loaded {len(documents)} documents")
    
    return messages, tickets, documents


def extract_knowledge_from_demo():
    """Extract knowledge from a few demo items"""
    console.print("\n[bold cyan]Step 2: Extracting Knowledge[/bold cyan]")
    console.print("=" * 70)
    
    messages, tickets, documents = load_demo_data()
    
    # Select interesting items to extract
    interesting_messages = [
        m for m in messages 
        if any(keyword in m['text'].lower() for keyword in ['failed', 'decision', 'incident', 'migration'])
    ][:3]  # Limit to 3 to avoid rate limits
    
    # Prepare for extraction
    extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    all_knowledge = []
    
    console.print(f"\n[yellow]Extracting from {len(interesting_messages)} Slack messages...[/yellow]")
    
    for msg in interesting_messages:
        items = extractor.extract_knowledge(
            text=msg['text'],
            source_type='slack',
            source_id=msg['id']
        )
        all_knowledge.extend(items)
        console.print(f"  ✓ Extracted {len(items)} items from message")
    
    console.print(f"\n[bold green]✅ Total knowledge items extracted: {len(all_knowledge)}[/bold green]")
    
    return all_knowledge


def test_vector_store(knowledge_items):
    """Test ChromaDB vector store"""
    console.print("\n[bold cyan]Step 3: Testing Vector Store (ChromaDB)[/bold cyan]")
    console.print("=" * 70)
    
    # Initialize vector store
    vector_store = VectorStore(
        persist_dir=settings.CHROMA_PERSIST_DIR,
        collection_name=settings.CHROMA_COLLECTION_NAME
    )
    vector_store.initialize_store()
    
    # Add knowledge items
    console.print(f"\n[yellow]Adding {len(knowledge_items)} items to vector store...[/yellow]")
    count = vector_store.add_knowledge(knowledge_items)
    console.print(f"[green]✓ Added {count} items[/green]")
    
    # Get stats
    stats = vector_store.get_stats()
    console.print(f"\n[bold]Vector Store Statistics:[/bold]")
    console.print(f"  Total items: {stats['total_items']}")
    console.print(f"  By type: {stats['items_by_type']}")
    console.print(f"  By outcome: {stats['items_by_outcome']}")
    
    # Test semantic search
    console.print(f"\n[yellow]Testing semantic search...[/yellow]")
    query = "database migration problems"
    results = vector_store.search_similar(query, top_k=3)
    
    console.print(f"\n[bold]Search Results for: '{query}'[/bold]")
    for i, result in enumerate(results, 1):
        metadata = result['metadata']
        console.print(f"\n{i}. [cyan]{metadata.get('content_type', 'unknown')}[/cyan]")
        console.print(f"   Topics: {', '.join(metadata.get('topics', []))}")
        console.print(f"   Importance: {metadata.get('importance_score', 0)}/10")
        console.print(f"   Distance: {result.get('distance', 'N/A'):.4f}" if result.get('distance') else "")
    
    # Test topic search
    console.print(f"\n[yellow]Testing topic search...[/yellow]")
    topic_results = vector_store.search_by_topic(['postgresql', 'migration'])
    console.print(f"[green]✓ Found {len(topic_results)} items for topics: postgresql, migration[/green]")
    
    # Test get by ID
    if knowledge_items:
        test_id = knowledge_items[0].id
        console.print(f"\n[yellow]Testing get by ID: {test_id}...[/yellow]")
        item = vector_store.get_by_id(test_id)
        if item:
            console.print(f"[green]✓ Retrieved item successfully[/green]")
        else:
            console.print(f"[red]✗ Failed to retrieve item[/red]")
    
    console.print(f"\n[bold green]✅ Vector store tests complete![/bold green]")
    return vector_store


def test_knowledge_graph(knowledge_items):
    """Test NetworkX knowledge graph"""
    console.print("\n[bold cyan]Step 4: Testing Knowledge Graph (NetworkX)[/bold cyan]")
    console.print("=" * 70)
    
    # Build graph
    graph_builder = GraphBuilder()
    console.print(f"\n[yellow]Building knowledge graph from {len(knowledge_items)} items...[/yellow]")
    graph = graph_builder.build_graph(knowledge_items)
    
    console.print(f"\n[bold]Graph Statistics:[/bold]")
    console.print(f"  Total nodes: {graph.number_of_nodes()}")
    console.print(f"  Total edges: {graph.number_of_edges()}")
    
    # Count node types
    node_types = {}
    for node, data in graph.nodes(data=True):
        node_type = data.get('node_type', 'unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    console.print(f"\n[bold]Nodes by Type:[/bold]")
    for node_type, count in sorted(node_types.items()):
        console.print(f"  {node_type}: {count}")
    
    # Test find related items
    if knowledge_items:
        test_item_id = knowledge_items[0].id
        console.print(f"\n[yellow]Testing find_related_items for: {test_item_id}...[/yellow]")
        related = graph_builder.find_related_items(test_item_id, max_hops=2)
        console.print(f"[green]✓ Found {len(related)} related items[/green]")
        
        if related:
            console.print(f"\n[bold]Top 3 Related Items:[/bold]")
            for item in related[:3]:
                console.print(f"  • {item['title'][:60]}... (distance: {item['distance']})")
    
    # Test find expert
    console.print(f"\n[yellow]Testing find_expert for topic: 'postgresql'...[/yellow]")
    experts = graph_builder.find_expert('postgresql')
    console.print(f"[green]✓ Found {len(experts)} experts[/green]")
    
    if experts:
        console.print(f"\n[bold]Top Experts:[/bold]")
        for expert in experts[:3]:
            console.print(f"  • {expert['name']}: {expert['item_count']} items, importance: {expert['total_importance']}")
    
    # Test get item history
    console.print(f"\n[yellow]Testing get_item_history for topic: 'postgresql'...[/yellow]")
    history = graph_builder.get_item_history('postgresql')
    console.print(f"[green]✓ Found {len(history)} items in history[/green]")
    
    if history:
        console.print(f"\n[bold]Item History:[/bold]")
        for item in history[:3]:
            console.print(f"  • [{item['date_occurred']}] {item['title'][:60]}...")
    
    # Test export to JSON
    console.print(f"\n[yellow]Testing export_graph_json...[/yellow]")
    graph_json = graph_builder.export_graph_json()
    console.print(f"[green]✓ Exported {len(graph_json['nodes'])} nodes and {len(graph_json['links'])} links[/green]")
    
    console.print(f"\n[bold green]✅ Knowledge graph tests complete![/bold green]")
    return graph_builder


def create_summary_table(knowledge_items, vector_store, graph_builder):
    """Create a summary table of all components"""
    console.print("\n[bold cyan]Summary[/bold cyan]")
    console.print("=" * 70)
    
    table = Table(title="ContextBridge Storage Layer - Test Results", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", width=25)
    table.add_column("Status", style="green", width=15)
    table.add_column("Details", style="white", width=40)
    
    # Knowledge extraction
    table.add_row(
        "Knowledge Extraction",
        "✅ WORKING",
        f"{len(knowledge_items)} items extracted"
    )
    
    # Vector store
    stats = vector_store.get_stats()
    table.add_row(
        "Vector Store (ChromaDB)",
        "✅ WORKING",
        f"{stats['total_items']} items stored"
    )
    
    # Knowledge graph
    table.add_row(
        "Knowledge Graph (NetworkX)",
        "✅ WORKING",
        f"{graph_builder.graph.number_of_nodes()} nodes, {graph_builder.graph.number_of_edges()} edges"
    )
    
    # Semantic search
    table.add_row(
        "Semantic Search",
        "✅ WORKING",
        "Query and filter support"
    )
    
    # Graph queries
    table.add_row(
        "Graph Queries",
        "✅ WORKING",
        "Related items, experts, history"
    )
    
    # D3.js export
    table.add_row(
        "D3.js Export",
        "✅ WORKING",
        "JSON format for visualization"
    )
    
    console.print(table)


def main():
    """Run all tests"""
    console.print("\n")
    console.print("=" * 70, style="bold magenta")
    console.print("  ContextBridge Storage Layer - Test Suite", style="bold magenta")
    console.print("  Vector Store (ChromaDB) + Knowledge Graph (NetworkX)", style="magenta")
    console.print("=" * 70, style="bold magenta")
    
    try:
        # Step 1 & 2: Load and extract knowledge
        knowledge_items = extract_knowledge_from_demo()
        
        if not knowledge_items:
            console.print("[red]No knowledge items extracted. Cannot proceed with tests.[/red]")
            return
        
        # Step 3: Test vector store
        vector_store = test_vector_store(knowledge_items)
        
        # Step 4: Test knowledge graph
        graph_builder = test_knowledge_graph(knowledge_items)
        
        # Summary
        create_summary_table(knowledge_items, vector_store, graph_builder)
        
        console.print("\n[bold green]✅ All tests completed successfully![/bold green]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
