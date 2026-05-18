"""
Test FastAPI Backend
Tests all API endpoints
"""

import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

BASE_URL = "http://localhost:8000/api"


def test_health():
    """Test health endpoint"""
    console.print("\n[bold cyan]1. Testing Health Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/health")
    console.print(f"Status: {response.status_code}")
    console.print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_demo_seed():
    """Test demo data seeding"""
    console.print("\n[bold cyan]2. Testing Demo Seed Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.post(f"{BASE_URL}/demo/seed")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Seeded {data['items_seeded']} items[/green]")
        console.print(f"Message: {data['message']}")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_stats():
    """Test stats endpoint"""
    console.print("\n[bold cyan]3. Testing Stats Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/stats")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]Total items: {data['total_knowledge_items']}[/green]")
        console.print(f"By type: {data['items_by_type']}")
        console.print(f"By outcome: {data['items_by_outcome']}")
        console.print(f"Top topics: {data['top_topics'][:3]}")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_search():
    """Test search endpoint"""
    console.print("\n[bold cyan]4. Testing Search Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/knowledge/search?q=database migration&limit=3")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Found {len(data)} items[/green]")
        for item in data:
            console.print(f"  • {item['content_type']}: {item['title'][:60]}...")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_jira_trigger():
    """Test Jira trigger endpoint"""
    console.print("\n[bold cyan]5. Testing Jira Trigger Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    payload = {
        "ticket_title": "Migrate database to PostgreSQL",
        "ticket_description": "We need to migrate our database from MySQL to PostgreSQL for better performance.",
        "created_by": "test_user"
    }
    
    response = requests.post(f"{BASE_URL}/trigger/jira", json=payload)
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            console.print(f"[yellow]⚠️ Alert Level: {data['alert_level']}[/yellow]")
            console.print(f"Confidence: {data['confidence_score']}%")
            console.print(f"Headline: {data['headline']}")
            console.print(f"Insight: {data['synthesized_insight'][:200]}...")
        else:
            console.print("[dim]No alert generated[/dim]")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_query():
    """Test query endpoint"""
    console.print("\n[bold cyan]6. Testing Query Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    payload = {
        "question": "Why do we use React?",
        "user_id": "test_user"
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Query answered[/green]")
        console.print(f"Confidence: {data['confidence_score']}%")
        console.print(f"Answer: {data['synthesized_insight'][:200]}...")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_demo_scenario():
    """Test demo scenario endpoint"""
    console.print("\n[bold cyan]7. Testing Demo Scenario Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.post(f"{BASE_URL}/demo/scenario/A")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[yellow]⚠️ Scenario A: The Mistake Prevented[/yellow]")
        console.print(f"Alert Level: {data['alert_level']}")
        console.print(f"Confidence: {data['confidence_score']}%")
        console.print(f"Headline: {data['headline']}")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_graph():
    """Test graph endpoint"""
    console.print("\n[bold cyan]8. Testing Graph Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/graph")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Graph exported[/green]")
        console.print(f"Nodes: {len(data['nodes'])}")
        console.print(f"Links: {len(data['links'])}")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def test_experts():
    """Test experts endpoint"""
    console.print("\n[bold cyan]9. Testing Experts Endpoint[/bold cyan]")
    console.print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/experts?topic=database")
    console.print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Found {len(data)} experts[/green]")
        for expert in data:
            console.print(f"  • {expert['name']}: relevance {expert['relevance_score']}")
    else:
        console.print(f"[red]✗ Failed: {response.text}[/red]")
    
    return response.status_code == 200


def main():
    """Run all API tests"""
    console.print("\n")
    console.print("=" * 70, style="bold magenta")
    console.print("  ContextBridge API Test Suite", style="bold magenta")
    console.print("  Testing all FastAPI endpoints", style="magenta")
    console.print("=" * 70, style="bold magenta")
    
    console.print("\n[yellow]Make sure the API server is running:[/yellow]")
    console.print("  python main.py")
    console.print()
    
    try:
        # Run tests
        results = []
        
        results.append(("Health Check", test_health()))
        results.append(("Demo Seed", test_demo_seed()))
        results.append(("Stats", test_stats()))
        results.append(("Search", test_search()))
        results.append(("Jira Trigger", test_jira_trigger()))
        results.append(("Query", test_query()))
        results.append(("Demo Scenario", test_demo_scenario()))
        results.append(("Graph Export", test_graph()))
        results.append(("Find Experts", test_experts()))
        
        # Summary
        console.print("\n[bold cyan]Test Summary[/bold cyan]")
        console.print("=" * 70)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Test", style="cyan", width=30)
        table.add_column("Status", style="green", width=15)
        
        for name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            table.add_row(name, status)
        
        console.print(table)
        
        passed_count = sum(1 for _, passed in results if passed)
        total_count = len(results)
        
        console.print(f"\n[bold]Results: {passed_count}/{total_count} tests passed[/bold]")
        
        if passed_count == total_count:
            console.print("[bold green]✅ All tests passed![/bold green]\n")
        else:
            console.print("[bold yellow]⚠️ Some tests failed[/bold yellow]\n")
        
    except requests.exceptions.ConnectionError:
        console.print("\n[bold red]❌ Connection Error![/bold red]")
        console.print("Make sure the API server is running:")
        console.print("  python main.py")
        console.print()
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
