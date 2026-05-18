"""
Setup Verification Script
Verifies that ContextBridge is properly configured
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)"


def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if env_path.exists():
        # Check if API key is set
        with open(env_path, 'r') as f:
            content = f.read()
            if "GEMINI_API_KEY=" in content and "your_" not in content:
                return True, ".env file exists with API key"
            return False, ".env file exists but API key not configured"
    return False, ".env file not found"


def check_directories():
    """Check if required directories exist"""
    required_dirs = [
        "ingestion", "processing", "intelligence",
        "api", "db", "demo"
    ]
    
    missing = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing.append(dir_name)
    
    if not missing:
        return True, "All directories present"
    return False, f"Missing: {', '.join(missing)}"


def check_requirements():
    """Check if requirements.txt exists"""
    req_path = Path("requirements.txt")
    if req_path.exists():
        return True, "requirements.txt found"
    return False, "requirements.txt not found"


def main():
    """Run all checks"""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]ContextBridge Setup Verification[/bold cyan]\n"
        "Checking your installation...",
        title="🔍 Setup Check"
    ))
    console.print("\n")
    
    # Create results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check", style="cyan", width=30)
    table.add_column("Status", width=10)
    table.add_column("Details", style="dim")
    
    checks = [
        ("Python Version", check_python_version()),
        ("Environment File", check_env_file()),
        ("Project Structure", check_directories()),
        ("Requirements File", check_requirements()),
    ]
    
    all_passed = True
    for check_name, (passed, details) in checks:
        status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
        table.add_row(check_name, status, details)
        if not passed:
            all_passed = False
    
    console.print(table)
    console.print("\n")
    
    if all_passed:
        console.print(Panel.fit(
            "[bold green]✅ All checks passed![/bold green]\n\n"
            "Next steps:\n"
            "1. Install dependencies: [cyan]pip install -r requirements.txt[/cyan]\n"
            "2. Start the server: [cyan]python main.py[/cyan]\n"
            "3. Visit: [cyan]http://localhost:8000/docs[/cyan]",
            title="🎉 Ready to Go"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]❌ Some checks failed[/bold red]\n\n"
            "Please fix the issues above before proceeding.\n"
            "See README.md for setup instructions.",
            title="⚠️ Action Required"
        ))
    
    console.print("\n")


if __name__ == "__main__":
    main()
