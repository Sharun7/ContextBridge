"""
Demo Scenarios
Pre-built demo scenarios for hackathon presentation
"""

import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

logger = logging.getLogger(__name__)
console = Console()


class DemoScenarios:
    """Pre-built demo scenarios"""
    
    @staticmethod
    def scenario_a():
        """Scenario A: The Mistake Prevented"""
        console.print("\n")
        
        panel_content = Text()
        panel_content.append("🚨 SCENARIO A: The Mistake Prevented\n\n", style="bold red")
        panel_content.append("Trigger: ", style="yellow bold")
        panel_content.append("New Jira ticket created\n", style="white")
        panel_content.append("Title: ", style="cyan bold")
        panel_content.append("Migrate primary database from MySQL to PostgreSQL\n\n", style="white")
        panel_content.append("Expected Response:\n", style="yellow bold")
        panel_content.append("• Surface the 2023 failed attempt with Sarah Chen's documentation\n", style="white")
        panel_content.append("• Warning about connection pooling issues\n", style="white")
        panel_content.append("• Recommendation to consult Sarah Chen before proceeding\n", style="white")
        panel_content.append("\nKey Evidence:\n", style="green bold")
        panel_content.append("• Post-mortem DOC-089\n", style="dim")
        panel_content.append("• Jira ticket ENG-1234 (Failed)\n", style="dim")
        panel_content.append("• Slack conversation in #engineering\n", style="dim")
        panel_content.append("• Cost: $500K, 3 months wasted\n", style="red dim")
        
        console.print(Panel(panel_content, title="[bold]Demo Scenario A[/bold]", border_style="red"))
    
    @staticmethod
    def scenario_b():
        """Scenario B: The Question Answered"""
        console.print("\n")
        
        panel_content = Text()
        panel_content.append("💡 SCENARIO B: The Question Answered\n\n", style="bold blue")
        panel_content.append("Trigger: ", style="yellow bold")
        panel_content.append("Natural language query\n", style="white")
        panel_content.append("Question: ", style="cyan bold")
        panel_content.append("Why do we use React instead of Vue for our frontend?\n\n", style="white")
        panel_content.append("Expected Response:\n", style="yellow bold")
        panel_content.append("• Surface the 2022 architecture debate from Slack\n", style="white")
        panel_content.append("• Show decision rationale with specific technical reasons\n", style="white")
        panel_content.append("• Include links to original discussions and decision documents\n", style="white")
        panel_content.append("\nKey Evidence:\n", style="green bold")
        panel_content.append("• ADR-015: Standardize on React\n", style="dim")
        panel_content.append("• Slack #architecture channel discussion\n", style="dim")
        panel_content.append("• Decision by James Wilson (Principal Architect)\n", style="dim")
        panel_content.append("• 5 specific reasons documented\n", style="blue dim")
        
        console.print(Panel(panel_content, title="[bold]Demo Scenario B[/bold]", border_style="blue"))
    
    @staticmethod
    def scenario_c():
        """Scenario C: The Expert Found"""
        console.print("\n")
        
        panel_content = Text()
        panel_content.append("🧠 SCENARIO C: The Expert Found\n\n", style="bold green")
        panel_content.append("Trigger: ", style="yellow bold")
        panel_content.append("Natural language query\n", style="white")
        panel_content.append("Question: ", style="cyan bold")
        panel_content.append("Who in our team has experience with database migrations?\n\n", style="white")
        panel_content.append("Expected Response:\n", style="yellow bold")
        panel_content.append("• Return Sarah Chen as primary expert\n", style="white")
        panel_content.append("• Show evidence: Led PostgreSQL migration attempt in 2023\n", style="white")
        panel_content.append("• Include 2 other team members with relevant experience\n", style="white")
        panel_content.append("\nExperts Found:\n", style="green bold")
        panel_content.append("1. Sarah Chen - Senior Backend Engineer\n", style="dim")
        panel_content.append("   Evidence: Led ENG-1234, wrote DOC-089\n", style="dim")
        panel_content.append("2. Maria Garcia - DevOps Lead\n", style="dim")
        panel_content.append("   Evidence: Infrastructure for migration\n", style="dim")
        panel_content.append("3. Priya Patel - Data Engineer\n", style="dim")
        panel_content.append("   Evidence: Data Warehouse Migration 2023\n", style="dim")
        
        console.print(Panel(panel_content, title="[bold]Demo Scenario C[/bold]", border_style="green"))
    
    @staticmethod
    def show_all():
        """Show all scenarios"""
        console.print("\n")
        console.print("═" * 70, style="bold magenta")
        console.print("   ContextBridge - Demo Scenarios for TechEx Hackathon", style="bold magenta")
        console.print("   Track 4: Data & Intelligence | Team NexaCore", style="magenta")
        console.print("═" * 70, style="bold magenta")
        
        # Company info
        console.print("\n📊 Demo Company: ", style="bold cyan", end="")
        console.print("NovaTech Solutions (500-person software company)", style="white")
        console.print("📅 Time Period: ", style="bold cyan", end="")
        console.print("2022-2024 (3 years of institutional memory)", style="white")
        console.print("👥 Key People: ", style="bold cyan", end="")
        console.print("Sarah Chen, James Wilson, Emily Rodriguez, Alex Kumar", style="white")
        
        DemoScenarios.scenario_a()
        DemoScenarios.scenario_b()
        DemoScenarios.scenario_c()
        
        # Summary table
        console.print("\n")
        table = Table(title="Demo Scenario Summary", show_header=True, header_style="bold magenta")
        table.add_column("Scenario", style="cyan", width=20)
        table.add_column("Type", style="yellow", width=15)
        table.add_column("Value Demonstrated", style="green", width=35)
        
        table.add_row(
            "A: Mistake Prevented",
            "Proactive Alert",
            "Prevents $500K mistake by surfacing past failure"
        )
        table.add_row(
            "B: Question Answered",
            "Knowledge Query",
            "Instant access to 2-year-old decision rationale"
        )
        table.add_row(
            "C: Expert Found",
            "Expertise Discovery",
            "Finds right person with evidence in seconds"
        )
        
        console.print(table)
        
        console.print("\n[bold green]✅ All scenarios ready for demo![/bold green]")
        console.print("[dim]Run these scenarios via the API endpoints or demo UI[/dim]\n")


if __name__ == "__main__":
    DemoScenarios.show_all()
