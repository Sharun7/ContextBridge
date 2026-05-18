"""
Visualize Knowledge Graph Structure
Shows the graph structure in a readable format
"""

import json
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel

from processing.graph_builder import GraphBuilder
from processing.knowledge_extractor import KnowledgeItem

console = Console()


def create_sample_items():
    """Create sample knowledge items for visualization"""
    items = [
        KnowledgeItem({
            'id': 'item_1',
            'content_type': 'failure',
            'title': 'PostgreSQL Migration Failed',
            'summary': 'Database migration failed due to connection pooling issues',
            'key_facts': ['Connection pool exhaustion', 'pgBouncer misconfigured'],
            'people_involved': ['Sarah Chen', 'Maria Garcia'],
            'teams_involved': ['engineering', 'devops'],
            'topics': ['postgresql', 'migration', 'database', 'incident'],
            'outcome': 'failure',
            'importance_score': 9,
            'source_type': 'slack',
            'source_reference': 'msg_123',
            'date_occurred': '2023-09'
        }),
        KnowledgeItem({
            'id': 'item_2',
            'content_type': 'decision',
            'title': 'Standardized on React',
            'summary': 'Team decided to use React for all frontend development',
            'key_facts': ['Better TypeScript support', 'Larger ecosystem'],
            'people_involved': ['James Wilson', 'Lisa Park'],
            'teams_involved': ['engineering', 'product'],
            'topics': ['react', 'frontend', 'architecture', 'decision'],
            'outcome': 'success',
            'importance_score': 7,
            'source_type': 'document',
            'source_reference': 'ADR-015',
            'date_occurred': '2022-03'
        }),
        KnowledgeItem({
            'id': 'item_3',
            'content_type': 'lesson',
            'title': 'Always Load Test Before Migration',
            'summary': 'Critical lesson learned from failed PostgreSQL migration',
            'key_facts': ['Load testing is mandatory', 'Test with production traffic'],
            'people_involved': ['Sarah Chen'],
            'teams_involved': ['engineering'],
            'topics': ['database', 'migration', 'testing', 'best-practices'],
            'outcome': 'success',
            'importance_score': 8,
            'source_type': 'document',
            'source_reference': 'DOC-089',
            'date_occurred': '2023-09'
        })
    ]
    return items


def visualize_graph_structure():
    """Visualize the knowledge graph structure"""
    console.print("\n[bold cyan]Knowledge Graph Structure Visualization[/bold cyan]")
    console.print("=" * 70)
    
    # Create sample items
    items = create_sample_items()
    
    # Build graph
    builder = GraphBuilder()
    graph = builder.build_graph(items)
    
    # Create tree visualization
    tree = Tree("[bold magenta]Knowledge Graph[/bold magenta]")
    
    # Group nodes by type
    node_types = {}
    for node, data in graph.nodes(data=True):
        node_type = data.get('node_type', 'unknown')
        if node_type not in node_types:
            node_types[node_type] = []
        node_types[node_type].append((node, data))
    
    # Add branches for each node type
    for node_type, nodes in sorted(node_types.items()):
        type_branch = tree.add(f"[bold yellow]{node_type.upper()} ({len(nodes)} nodes)[/bold yellow]")
        
        for node_id, data in nodes[:5]:  # Show first 5 of each type
            if node_type == 'knowledge_item':
                label = f"[cyan]{data.get('title', node_id)[:50]}[/cyan]"
                node_branch = type_branch.add(label)
                node_branch.add(f"Type: {data.get('content_type', 'unknown')}")
                node_branch.add(f"Importance: {data.get('importance_score', 0)}/10")
                node_branch.add(f"Outcome: {data.get('outcome', 'unknown')}")
            else:
                label = f"[green]{data.get('name', node_id)}[/green]"
                type_branch.add(label)
        
        if len(nodes) > 5:
            type_branch.add(f"[dim]... and {len(nodes) - 5} more[/dim]")
    
    console.print(tree)
    
    # Show edge statistics
    console.print(f"\n[bold]Edge Statistics:[/bold]")
    edge_types = {}
    for u, v, data in graph.edges(data=True):
        edge_type = data.get('edge_type', 'unknown')
        edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
    
    for edge_type, count in sorted(edge_types.items()):
        console.print(f"  {edge_type}: {count} edges")
    
    # Show sample queries
    console.print(f"\n[bold cyan]Sample Graph Queries:[/bold cyan]")
    console.print("=" * 70)
    
    # Find related items
    console.print(f"\n[yellow]1. Find Related Items to 'PostgreSQL Migration Failed':[/yellow]")
    related = builder.find_related_items('item_1', max_hops=2)
    for item in related:
        console.print(f"   • {item['title']} (distance: {item['distance']})")
    
    # Find experts
    console.print(f"\n[yellow]2. Find Experts on 'database':[/yellow]")
    experts = builder.find_expert('database')
    for expert in experts:
        console.print(f"   • {expert['name']}: {expert['item_count']} items, importance: {expert['total_importance']}")
    
    # Get history
    console.print(f"\n[yellow]3. Get History for 'migration':[/yellow]")
    history = builder.get_item_history('migration')
    for item in history:
        console.print(f"   • [{item['date_occurred']}] {item['title']}")
    
    # Export to JSON
    console.print(f"\n[yellow]4. Export to D3.js Format:[/yellow]")
    graph_json = builder.export_graph_json()
    console.print(f"   Nodes: {len(graph_json['nodes'])}")
    console.print(f"   Links: {len(graph_json['links'])}")
    
    # Show sample node
    if graph_json['nodes']:
        sample_node = graph_json['nodes'][0]
        console.print(f"\n[bold]Sample Node (JSON):[/bold]")
        console.print(Panel(
            json.dumps(sample_node, indent=2),
            title="Node Structure",
            border_style="cyan"
        ))
    
    # Show sample link
    if graph_json['links']:
        sample_link = graph_json['links'][0]
        console.print(f"\n[bold]Sample Link (JSON):[/bold]")
        console.print(Panel(
            json.dumps(sample_link, indent=2),
            title="Link Structure",
            border_style="cyan"
        ))
    
    console.print(f"\n[bold green]✅ Graph visualization complete![/bold green]\n")


if __name__ == "__main__":
    visualize_graph_structure()
