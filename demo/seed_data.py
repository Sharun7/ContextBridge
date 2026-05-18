"""
Demo Data Generator
Generates realistic enterprise data for NovaTech Solutions
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

logger = logging.getLogger(__name__)


class DemoDataGenerator:
    """Generate realistic demo data for ContextBridge"""
    
    def __init__(self):
        self.output_dir = Path("demo/data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.company_name = "NovaTech Solutions"
    
    def generate_all(self):
        """Generate all demo data files"""
        print(f"\n🏢 Generating demo data for {self.company_name}...")
        print("=" * 60)
        
        self.generate_people()
        self.generate_slack_messages()
        self.generate_jira_tickets()
        self.generate_documents()
        
        print("\n✅ Demo data generation complete!")
        print(f"📁 Files saved to: {self.output_dir.absolute()}\n")
    
    def generate_people(self):
        """Generate people directory"""
        print("👥 Generating people directory...")
        
        people = [
            {
                "id": "sarah.chen",
                "name": "Sarah Chen",
                "role": "Senior Backend Engineer",
                "department": "Engineering",
                "email": "sarah.chen@novatech.com",
                "expertise_areas": ["PostgreSQL", "Database Architecture", "Python", "Microservices"],
                "past_projects": [
                    "PostgreSQL Migration Attempt (2023) - Lead",
                    "Microservices Refactoring (2022)",
                    "Payment Gateway Integration (2023)"
                ]
            },
            {
                "id": "james.wilson",
                "name": "James Wilson",
                "role": "Principal Architect",
                "department": "Engineering",
                "email": "james.wilson@novatech.com",
                "expertise_areas": ["System Architecture", "React", "Frontend", "Technical Strategy"],
                "past_projects": [
                    "React vs Vue Evaluation (2022) - Lead",
                    "Frontend Architecture Redesign (2022)",
                    "APAC Expansion Technical Planning (2024)"
                ]
            },
            {
                "id": "maria.garcia",
                "name": "Maria Garcia",
                "role": "DevOps Lead",
                "department": "Engineering",
                "email": "maria.garcia@novatech.com",
                "expertise_areas": ["Kubernetes", "CI/CD", "Database Operations", "AWS"],
                "past_projects": [
                    "PostgreSQL Migration Attempt (2023) - Infrastructure",
                    "Microservices Deployment Pipeline (2022)",
                    "Database Performance Optimization (2023)"
                ]
            },
            {
                "id": "alex.kumar",
                "name": "Alex Kumar",
                "role": "Staff Engineer",
                "department": "Engineering",
                "email": "alex.kumar@novatech.com",
                "expertise_areas": ["Payment Systems", "API Design", "Node.js", "Stripe Integration"],
                "past_projects": [
                    "Stripe vs Braintree Evaluation (2023) - Lead",
                    "Payment Gateway Migration (2023)",
                    "API Gateway Implementation (2022)"
                ]
            },
            {
                "id": "emily.rodriguez",
                "name": "Emily Rodriguez",
                "role": "Product Manager",
                "department": "Product",
                "email": "emily.rodriguez@novatech.com",
                "expertise_areas": ["Product Strategy", "Market Expansion", "Compliance", "User Research"],
                "past_projects": [
                    "APAC Market Expansion (2024) - Lead",
                    "Payment Features Roadmap (2023)",
                    "Mobile App Launch (2022)"
                ]
            },
            {
                "id": "david.thompson",
                "name": "David Thompson",
                "role": "Engineering Manager",
                "department": "Engineering",
                "email": "david.thompson@novatech.com",
                "expertise_areas": ["Team Leadership", "Microservices", "Java", "System Design"],
                "past_projects": [
                    "Microservices Refactoring (2022) - Lead",
                    "Team Scaling Initiative (2023)",
                    "Technical Debt Reduction (2024)"
                ]
            },
            {
                "id": "lisa.park",
                "name": "Lisa Park",
                "role": "Senior Frontend Engineer",
                "department": "Engineering",
                "email": "lisa.park@novatech.com",
                "expertise_areas": ["React", "TypeScript", "UI/UX", "Performance Optimization"],
                "past_projects": [
                    "React Migration (2022)",
                    "Design System Implementation (2023)",
                    "Mobile Responsive Redesign (2024)"
                ]
            },
            {
                "id": "michael.oconnor",
                "name": "Michael O'Connor",
                "role": "Security Engineer",
                "department": "Security",
                "email": "michael.oconnor@novatech.com",
                "expertise_areas": ["Application Security", "Compliance", "GDPR", "Penetration Testing"],
                "past_projects": [
                    "APAC Compliance Assessment (2024)",
                    "Security Audit (2023)",
                    "SOC 2 Certification (2022)"
                ]
            },
            {
                "id": "priya.patel",
                "name": "Priya Patel",
                "role": "Data Engineer",
                "department": "Engineering",
                "email": "priya.patel@novatech.com",
                "expertise_areas": ["Data Pipelines", "PostgreSQL", "ETL", "Analytics"],
                "past_projects": [
                    "Data Warehouse Migration (2023)",
                    "Analytics Platform (2022)",
                    "Real-time Data Processing (2024)"
                ]
            },
            {
                "id": "robert.zhang",
                "name": "Robert Zhang",
                "role": "QA Lead",
                "department": "Engineering",
                "email": "robert.zhang@novatech.com",
                "expertise_areas": ["Test Automation", "Quality Assurance", "CI/CD", "Performance Testing"],
                "past_projects": [
                    "Automated Testing Framework (2023)",
                    "Load Testing Infrastructure (2022)",
                    "Quality Metrics Dashboard (2024)"
                ]
            }
        ]
        
        # Add 10 more team members
        additional_people = [
            {"id": "jennifer.lee", "name": "Jennifer Lee", "role": "Backend Engineer", "department": "Engineering"},
            {"id": "carlos.mendez", "name": "Carlos Mendez", "role": "Frontend Engineer", "department": "Engineering"},
            {"id": "amanda.white", "name": "Amanda White", "role": "Product Designer", "department": "Design"},
            {"id": "kevin.brown", "name": "Kevin Brown", "role": "Backend Engineer", "department": "Engineering"},
            {"id": "sophia.anderson", "name": "Sophia Anderson", "role": "Technical Writer", "department": "Engineering"},
            {"id": "daniel.martinez", "name": "Daniel Martinez", "role": "SRE Engineer", "department": "Engineering"},
            {"id": "olivia.taylor", "name": "Olivia Taylor", "role": "Product Manager", "department": "Product"},
            {"id": "ryan.jackson", "name": "Ryan Jackson", "role": "Data Analyst", "department": "Analytics"},
            {"id": "natalie.kim", "name": "Natalie Kim", "role": "UX Researcher", "department": "Design"},
            {"id": "thomas.nguyen", "name": "Thomas Nguyen", "role": "DevOps Engineer", "department": "Engineering"}
        ]
        
        for person in additional_people:
            person["email"] = f"{person['id']}@novatech.com"
            person["expertise_areas"] = ["Software Development", "Agile", "Collaboration"]
            person["past_projects"] = ["Various projects (2022-2024)"]
        
        people.extend(additional_people)
        
        output_file = self.output_dir / "people.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(people, f, indent=2)
        
        print(f"   ✓ Generated {len(people)} employees")

    
    def generate_slack_messages(self):
        """Generate Slack messages"""
        print("💬 Generating Slack messages...")
        
        messages = []
        
        # PostgreSQL Migration Failure (Q3 2023) - #engineering
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-07-15T10:30:00Z",
                "text": "Hey team, I'm starting the PostgreSQL migration project this week. We're moving from MySQL to PostgreSQL for better JSON support and performance. Will keep everyone updated!"
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "maria.garcia",
                "username": "Maria Garcia",
                "timestamp": "2023-07-15T10:35:00Z",
                "text": "@sarah.chen Sounds good! Make sure to test connection pooling thoroughly. We had issues with that in the past."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-08-22T14:20:00Z",
                "text": "Update on PostgreSQL migration: We're seeing some weird connection pooling behavior in staging. Connections aren't being released properly. Investigating..."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "david.thompson",
                "username": "David Thompson",
                "timestamp": "2023-08-22T14:45:00Z",
                "text": "@sarah.chen How critical is this? Do we need to pause the migration?"
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-09-10T16:00:00Z",
                "text": "Bad news team. The PostgreSQL migration is failing. Connection pool exhaustion is causing cascading failures. We're seeing 500 errors in production. Rolling back now."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#incidents",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-09-10T16:15:00Z",
                "text": "🚨 INCIDENT: PostgreSQL migration caused production outage. Root cause: pgBouncer connection pooling misconfiguration. Max connections set too low (100) for our traffic. Should have been 500+. Rollback complete. Service restored."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "maria.garcia",
                "username": "Maria Garcia",
                "timestamp": "2023-09-11T09:00:00Z",
                "text": "Post-mortem scheduled for tomorrow. Key lesson: always load test with production-level traffic before migrating databases. The connection pool settings were never stress tested."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-09-12T11:30:00Z",
                "text": "I've documented everything in the post-mortem doc. TL;DR: Don't attempt PostgreSQL migration without proper connection pool configuration and load testing. Cost us 3 months of work."
            }
        ])
        
        # React vs Vue Debate (2022) - #architecture
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "james.wilson",
                "username": "James Wilson",
                "timestamp": "2022-03-10T10:00:00Z",
                "text": "Opening discussion: Should we standardize on React or Vue for our frontend? We currently have a mix and it's causing maintenance issues."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "lisa.park",
                "username": "Lisa Park",
                "timestamp": "2022-03-10T10:15:00Z",
                "text": "I vote React. Larger ecosystem, better TypeScript support, and more engineers in the market know it. Easier to hire."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "carlos.mendez",
                "username": "Carlos Mendez",
                "timestamp": "2022-03-10T10:20:00Z",
                "text": "Vue has a gentler learning curve though. And the documentation is excellent."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "james.wilson",
                "username": "James Wilson",
                "timestamp": "2022-03-15T14:30:00Z",
                "text": "After evaluating both, here's my recommendation: React. Reasons: 1) Better TypeScript integration 2) Larger talent pool 3) More third-party libraries 4) Better mobile story with React Native 5) Our team already knows it better"
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "david.thompson",
                "username": "David Thompson",
                "timestamp": "2022-03-15T15:00:00Z",
                "text": "Agreed. Let's go with React. I'll create an ADR documenting this decision."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "james.wilson",
                "username": "James Wilson",
                "timestamp": "2022-03-20T09:00:00Z",
                "text": "ADR-015 published: 'Standardize on React for Frontend Development'. All new projects must use React. Vue projects will be migrated over the next 6 months."
            }
        ])
        
        # APAC Expansion (2024) - #product
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#product",
                "user": "emily.rodriguez",
                "username": "Emily Rodriguez",
                "timestamp": "2024-01-15T10:00:00Z",
                "text": "Exciting news! We're planning to expand to APAC markets (Singapore, Japan, Australia) in Q2 2024. This is a huge opportunity for growth."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#product",
                "user": "michael.oconnor",
                "username": "Michael O'Connor",
                "timestamp": "2024-01-15T10:30:00Z",
                "text": "@emily.rodriguez We need to review GDPR, PDPA (Singapore), and APPI (Japan) compliance requirements. This is complex."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#product",
                "user": "emily.rodriguez",
                "username": "Emily Rodriguez",
                "timestamp": "2024-02-20T14:00:00Z",
                "text": "Update: APAC expansion is more complex than expected. Data residency requirements mean we need infrastructure in each country. Legal review ongoing."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#product",
                "user": "james.wilson",
                "username": "James Wilson",
                "timestamp": "2024-03-10T11:00:00Z",
                "text": "Technical requirements for APAC: separate database instances per region, data encryption at rest, audit logging for all data access. This is a 6-month project minimum."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#product",
                "user": "emily.rodriguez",
                "username": "Emily Rodriguez",
                "timestamp": "2024-04-05T16:00:00Z",
                "text": "Difficult decision: We're pausing APAC expansion. Compliance requirements are too complex for our current resources. We need to hire specialized legal and engineering talent first. Revisiting in 2025."
            }
        ])
        
        # Microservices Success (2022) - #engineering
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "david.thompson",
                "username": "David Thompson",
                "timestamp": "2022-05-01T09:00:00Z",
                "text": "Starting the microservices refactoring project. We're breaking the monolith into: Auth Service, User Service, Payment Service, Notification Service. Timeline: 4 months."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2022-05-01T09:30:00Z",
                "text": "I'll take the Payment Service. This will integrate with our Stripe setup."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "david.thompson",
                "username": "David Thompson",
                "timestamp": "2022-08-15T14:00:00Z",
                "text": "Microservices migration complete! All services deployed to production. Performance improved by 40%, deployment time reduced from 30min to 5min per service. This was a huge success."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "maria.garcia",
                "username": "Maria Garcia",
                "timestamp": "2022-08-15T14:30:00Z",
                "text": "Great work team! The Kubernetes setup is running smoothly. Auto-scaling is working perfectly."
            }
        ])
        
        # Stripe vs Braintree (2023) - #engineering
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "alex.kumar",
                "username": "Alex Kumar",
                "timestamp": "2023-04-10T10:00:00Z",
                "text": "We need to choose a payment gateway: Stripe vs Braintree. I'm doing a technical evaluation this week."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "alex.kumar",
                "username": "Alex Kumar",
                "timestamp": "2023-04-20T15:00:00Z",
                "text": "Evaluation complete. Stripe wins. Better API, superior documentation, more payment methods, excellent webhook system, and better fraud detection. Braintree is good but Stripe is better for our use case."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "sarah.chen",
                "username": "Sarah Chen",
                "timestamp": "2023-04-20T15:15:00Z",
                "text": "@alex.kumar Agreed. Stripe's API is much cleaner. Integration will be easier."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "alex.kumar",
                "username": "Alex Kumar",
                "timestamp": "2023-05-01T09:00:00Z",
                "text": "Stripe integration complete and deployed to production. Processing payments smoothly. No issues so far."
            }
        ])
        
        # Additional context messages
        messages.extend([
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "priya.patel",
                "username": "Priya Patel",
                "timestamp": "2023-11-10T10:00:00Z",
                "text": "Reminder: Always document your architectural decisions. Future you (and your teammates) will thank you."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#architecture",
                "user": "james.wilson",
                "username": "James Wilson",
                "timestamp": "2024-01-05T11:00:00Z",
                "text": "New year, new projects! Let's make sure we learn from past mistakes. Read the post-mortems before starting similar projects."
            },
            {
                "id": str(uuid.uuid4()),
                "channel": "#engineering",
                "user": "robert.zhang",
                "username": "Robert Zhang",
                "timestamp": "2024-02-15T14:00:00Z",
                "text": "QA tip: Load testing is not optional. It's mandatory for any infrastructure change. We learned this the hard way."
            }
        ])
        
        output_file = self.output_dir / "slack_messages.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2)
        
        print(f"   ✓ Generated {len(messages)} Slack messages across 4 channels")

    
    def generate_jira_tickets(self):
        """Generate Jira tickets"""
        print("🎫 Generating Jira tickets...")
        
        tickets = []
        
        # PostgreSQL Migration tickets
        tickets.extend([
            {
                "id": "ENG-1234",
                "project": "Engineering",
                "title": "Migrate primary database from MySQL to PostgreSQL",
                "description": "We need to migrate our primary database from MySQL to PostgreSQL to take advantage of better JSON support, improved performance, and advanced indexing capabilities.",
                "status": "Closed",
                "resolution": "Failed",
                "priority": "High",
                "assignee": "sarah.chen",
                "reporter": "david.thompson",
                "created": "2023-07-10T09:00:00Z",
                "updated": "2023-09-12T17:00:00Z",
                "labels": ["database", "migration", "postgresql"],
                "comments": [
                    {
                        "author": "sarah.chen",
                        "timestamp": "2023-07-15T10:00:00Z",
                        "text": "Starting work on this. Will set up PostgreSQL instance in staging first."
                    },
                    {
                        "author": "maria.garcia",
                        "timestamp": "2023-08-22T15:00:00Z",
                        "text": "Seeing connection pooling issues in staging. pgBouncer configuration needs review."
                    },
                    {
                        "author": "sarah.chen",
                        "timestamp": "2023-09-10T16:30:00Z",
                        "text": "CRITICAL: Migration failed in production. Connection pool exhaustion caused cascading failures. Rolling back immediately."
                    },
                    {
                        "author": "david.thompson",
                        "timestamp": "2023-09-12T17:00:00Z",
                        "text": "Closing as Failed. Root cause: pgBouncer max_connections set to 100, should have been 500+. Never load tested with production traffic levels. See post-mortem DOC-089."
                    }
                ]
            },
            {
                "id": "ENG-1235",
                "project": "Engineering",
                "title": "Post-mortem: PostgreSQL Migration Failure",
                "description": "Document lessons learned from the failed PostgreSQL migration attempt in Q3 2023.",
                "status": "Closed",
                "resolution": "Done",
                "priority": "High",
                "assignee": "sarah.chen",
                "reporter": "david.thompson",
                "created": "2023-09-11T09:00:00Z",
                "updated": "2023-09-13T16:00:00Z",
                "labels": ["post-mortem", "database", "incident"],
                "comments": [
                    {
                        "author": "sarah.chen",
                        "timestamp": "2023-09-13T16:00:00Z",
                        "text": "Post-mortem complete. Key findings: 1) Connection pool misconfigured 2) No load testing with production traffic 3) Insufficient monitoring during migration. Recommendations: Always load test, proper connection pool sizing, gradual rollout strategy."
                    }
                ]
            }
        ])
        
        # React vs Vue ADR
        tickets.append({
            "id": "ARCH-045",
            "project": "Architecture",
            "title": "ADR: Standardize on React for Frontend Development",
            "description": "Architecture Decision Record: After evaluating React and Vue, we are standardizing on React for all frontend development.",
            "status": "Closed",
            "resolution": "Done",
            "priority": "Medium",
            "assignee": "james.wilson",
            "reporter": "james.wilson",
            "created": "2022-03-10T10:00:00Z",
            "updated": "2022-03-20T10:00:00Z",
            "labels": ["adr", "frontend", "react", "architecture"],
            "comments": [
                {
                    "author": "james.wilson",
                    "timestamp": "2022-03-20T10:00:00Z",
                    "text": "Decision: React. Rationale: 1) Better TypeScript support 2) Larger ecosystem and community 3) Easier hiring (more React developers) 4) React Native for mobile 5) Team familiarity. All new projects use React. Vue projects migrate over 6 months."
                }
            ]
        })
        
        # APAC Expansion tickets
        tickets.extend([
            {
                "id": "PROD-567",
                "project": "Product",
                "title": "APAC Market Expansion - Technical Requirements",
                "description": "Define technical requirements for expanding to APAC markets (Singapore, Japan, Australia).",
                "status": "On Hold",
                "resolution": "Unresolved",
                "priority": "High",
                "assignee": "emily.rodriguez",
                "reporter": "emily.rodriguez",
                "created": "2024-01-15T10:00:00Z",
                "updated": "2024-04-05T16:30:00Z",
                "labels": ["apac", "expansion", "compliance"],
                "comments": [
                    {
                        "author": "michael.oconnor",
                        "timestamp": "2024-01-20T11:00:00Z",
                        "text": "Compliance requirements: PDPA (Singapore), APPI (Japan), Privacy Act (Australia). Data residency required for each country."
                    },
                    {
                        "author": "james.wilson",
                        "timestamp": "2024-03-10T11:30:00Z",
                        "text": "Technical requirements: Separate DB instances per region, encryption at rest, audit logging, region-specific infrastructure. Estimated 6 months development."
                    },
                    {
                        "author": "emily.rodriguez",
                        "timestamp": "2024-04-05T16:30:00Z",
                        "text": "Pausing this initiative. Compliance complexity too high for current resources. Need specialized legal and engineering hires. Revisiting in 2025."
                    }
                ]
            }
        ])
        
        # Microservices tickets
        tickets.extend([
            {
                "id": "ENG-890",
                "project": "Engineering",
                "title": "Microservices Refactoring - Break Monolith",
                "description": "Refactor monolithic application into microservices: Auth, User, Payment, Notification services.",
                "status": "Closed",
                "resolution": "Done",
                "priority": "High",
                "assignee": "david.thompson",
                "reporter": "david.thompson",
                "created": "2022-05-01T09:00:00Z",
                "updated": "2022-08-15T15:00:00Z",
                "labels": ["microservices", "architecture", "refactoring"],
                "comments": [
                    {
                        "author": "david.thompson",
                        "timestamp": "2022-08-15T15:00:00Z",
                        "text": "SUCCESS! All services deployed. Performance improved 40%, deployment time reduced from 30min to 5min per service. Kubernetes auto-scaling working perfectly."
                    }
                ]
            }
        ])
        
        # Stripe vs Braintree
        tickets.extend([
            {
                "id": "ENG-1100",
                "project": "Engineering",
                "title": "Payment Gateway Evaluation: Stripe vs Braintree",
                "description": "Evaluate and choose between Stripe and Braintree for payment processing.",
                "status": "Closed",
                "resolution": "Done",
                "priority": "High",
                "assignee": "alex.kumar",
                "reporter": "alex.kumar",
                "created": "2023-04-10T10:00:00Z",
                "updated": "2023-04-20T16:00:00Z",
                "labels": ["payment", "vendor-evaluation", "stripe"],
                "comments": [
                    {
                        "author": "alex.kumar",
                        "timestamp": "2023-04-20T16:00:00Z",
                        "text": "Decision: Stripe. Better API design, superior documentation, more payment methods, excellent webhooks, better fraud detection. Integration completed successfully."
                    }
                ]
            }
        ])
        
        # Additional tickets for context
        tickets.extend([
            {
                "id": "ENG-1500",
                "project": "Engineering",
                "title": "Implement automated load testing for infrastructure changes",
                "description": "Create automated load testing pipeline to prevent incidents like the PostgreSQL migration failure.",
                "status": "In Progress",
                "resolution": "Unresolved",
                "priority": "High",
                "assignee": "robert.zhang",
                "reporter": "maria.garcia",
                "created": "2023-09-15T10:00:00Z",
                "updated": "2024-01-10T14:00:00Z",
                "labels": ["testing", "infrastructure", "automation"],
                "comments": []
            },
            {
                "id": "ENG-1600",
                "project": "Engineering",
                "title": "Database connection pool monitoring and alerting",
                "description": "Implement monitoring and alerting for database connection pool usage to prevent exhaustion.",
                "status": "Closed",
                "resolution": "Done",
                "priority": "High",
                "assignee": "maria.garcia",
                "reporter": "sarah.chen",
                "created": "2023-09-20T09:00:00Z",
                "updated": "2023-10-15T16:00:00Z",
                "labels": ["monitoring", "database", "observability"],
                "comments": []
            }
        ])
        
        output_file = self.output_dir / "jira_tickets.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, indent=2)
        
        print(f"   ✓ Generated {len(tickets)} Jira tickets")

    
    def generate_documents(self):
        """Generate documents"""
        print("📄 Generating documents...")
        
        documents = []
        
        # ADR: React Decision
        documents.append({
            "id": "ADR-015",
            "title": "Architecture Decision Record: Standardize on React for Frontend Development",
            "type": "Architecture Decision Record",
            "author": "james.wilson",
            "date": "2022-03-20",
            "folder": "Architecture/ADRs",
            "content": """# ADR-015: Standardize on React for Frontend Development

## Status
Accepted

## Context
We currently have a mix of React and Vue components across our frontend applications. This creates maintenance overhead, makes it harder to share code, and complicates hiring and onboarding.

## Decision
We will standardize on React for all frontend development.

## Rationale
1. **TypeScript Integration**: React has superior TypeScript support with better type inference and tooling
2. **Ecosystem**: Larger ecosystem with more third-party libraries and components
3. **Talent Pool**: Easier to hire React developers - larger market availability
4. **Mobile Strategy**: React Native provides a path to mobile development with shared code
5. **Team Knowledge**: 80% of our frontend team already knows React well
6. **Community**: Larger community means better support and more resources

## Consequences
- All new frontend projects must use React
- Existing Vue projects will be migrated over the next 6 months
- Training will be provided for team members who need to learn React
- Standardized component library will be built in React

## Alternatives Considered
- **Vue**: Gentler learning curve, excellent documentation, but smaller ecosystem
- **Angular**: Enterprise-ready but too opinionated and heavyweight for our needs
"""
        })
        
        # Post-mortem: PostgreSQL Migration
        documents.append({
            "id": "DOC-089",
            "title": "Post-Mortem: PostgreSQL Migration Failure (Q3 2023)",
            "type": "Post-Mortem",
            "author": "sarah.chen",
            "date": "2023-09-13",
            "folder": "Engineering/Post-Mortems",
            "content": """# Post-Mortem: PostgreSQL Migration Failure

## Incident Summary
On September 10, 2023, our attempt to migrate from MySQL to PostgreSQL resulted in a production outage lasting 45 minutes. The migration was rolled back and the project was abandoned.

## Timeline
- **July 10, 2023**: Project initiated
- **July 15, 2023**: PostgreSQL instance set up in staging
- **August 22, 2023**: Connection pooling issues discovered in staging
- **September 10, 2023 16:00**: Migration deployed to production
- **September 10, 2023 16:15**: Production outage - 500 errors across all services
- **September 10, 2023 16:45**: Rollback completed, service restored

## Root Cause
pgBouncer connection pool was configured with max_connections=100, which was insufficient for production traffic levels (should have been 500+). Under load, the connection pool was exhausted, causing cascading failures across all services.

## What Went Wrong
1. **No Load Testing**: Never tested with production-level traffic
2. **Insufficient Monitoring**: No alerts for connection pool usage
3. **Configuration Error**: Connection pool settings copied from development environment
4. **Rushed Timeline**: Pressure to complete migration quickly led to skipped testing steps

## What Went Right
1. **Fast Rollback**: Rollback procedure was well-documented and executed quickly
2. **Good Communication**: Team communicated effectively during the incident
3. **Data Integrity**: No data loss occurred during the incident

## Lessons Learned
1. **Always load test infrastructure changes** with production-level traffic
2. **Proper connection pool sizing** is critical for database performance
3. **Gradual rollout** strategy should be used for major infrastructure changes
4. **Monitoring and alerting** must be in place before any migration

## Action Items
- [ ] Implement automated load testing pipeline (ENG-1500)
- [ ] Create connection pool monitoring and alerting (ENG-1600)
- [ ] Document database migration best practices
- [ ] Require load testing sign-off for all infrastructure changes

## Cost
- 3 months of engineering time wasted
- 45 minutes of production downtime
- Estimated cost: $500,000

## Recommendation
Do not attempt PostgreSQL migration again without:
1. Comprehensive load testing
2. Proper connection pool configuration
3. Gradual rollout strategy
4. Dedicated DBA review

**Author**: Sarah Chen  
**Date**: September 13, 2023  
**Reviewed by**: David Thompson, Maria Garcia
"""
        })
        
        # APAC Expansion Requirements
        documents.append({
            "id": "DOC-112",
            "title": "APAC Market Expansion - Technical Requirements",
            "type": "Technical Requirements",
            "author": "emily.rodriguez",
            "date": "2024-03-10",
            "folder": "Product/Market Expansion",
            "content": """# APAC Market Expansion - Technical Requirements

## Overview
Technical requirements for expanding NovaTech Solutions to APAC markets (Singapore, Japan, Australia).

## Compliance Requirements

### Singapore (PDPA - Personal Data Protection Act)
- Data residency: Customer data must be stored in Singapore
- Consent management: Explicit consent required for data collection
- Data breach notification: Within 72 hours

### Japan (APPI - Act on Protection of Personal Information)
- Data localization: Sensitive data must remain in Japan
- Cross-border transfer restrictions
- Anonymization requirements

### Australia (Privacy Act)
- Australian Privacy Principles (APPs) compliance
- Data breach notification scheme
- Cross-border disclosure rules

## Technical Architecture

### Infrastructure
- Separate database instances per country
- Regional data centers (AWS ap-southeast-1, ap-northeast-1, ap-southeast-2)
- Data encryption at rest and in transit
- Audit logging for all data access

### Development Effort
- Estimated timeline: 6 months
- Team size: 8 engineers + 2 legal consultants
- Cost estimate: $1.2M

## Current Status
**PAUSED** as of April 5, 2024

Compliance requirements are more complex than initially assessed. We need:
1. Specialized legal expertise in APAC data protection laws
2. Dedicated compliance engineering team
3. Regional infrastructure setup and management
4. Ongoing compliance monitoring and auditing

## Recommendation
Revisit in 2025 after hiring specialized talent and building compliance infrastructure.

**Author**: Emily Rodriguez  
**Contributors**: James Wilson, Michael O'Connor  
**Date**: March 10, 2024
"""
        })
        
        # Stripe vs Braintree Evaluation
        documents.append({
            "id": "DOC-095",
            "title": "Payment Gateway Evaluation: Stripe vs Braintree",
            "type": "Vendor Evaluation",
            "author": "alex.kumar",
            "date": "2023-04-20",
            "folder": "Engineering/Vendor Evaluations",
            "content": """# Payment Gateway Evaluation: Stripe vs Braintree

## Executive Summary
After comprehensive evaluation, **Stripe** is recommended as our payment gateway provider.

## Evaluation Criteria

### API Quality
- **Stripe**: ⭐⭐⭐⭐⭐ Excellent RESTful API, intuitive design, comprehensive SDKs
- **Braintree**: ⭐⭐⭐⭐ Good API but less intuitive

### Documentation
- **Stripe**: ⭐⭐⭐⭐⭐ Industry-leading documentation with interactive examples
- **Braintree**: ⭐⭐⭐ Adequate but less comprehensive

### Payment Methods
- **Stripe**: Credit cards, ACH, Apple Pay, Google Pay, 135+ currencies
- **Braintree**: Credit cards, PayPal, Venmo, Apple Pay

### Pricing
- **Stripe**: 2.9% + $0.30 per transaction
- **Braintree**: 2.9% + $0.30 per transaction (similar)

### Fraud Detection
- **Stripe**: Radar - ML-powered fraud detection, excellent
- **Braintree**: Basic fraud tools, less sophisticated

### Webhooks
- **Stripe**: Robust webhook system with retry logic and monitoring
- **Braintree**: Basic webhooks

### Developer Experience
- **Stripe**: ⭐⭐⭐⭐⭐ Excellent DX, great testing tools
- **Braintree**: ⭐⭐⭐ Good but not as polished

## Decision
**Stripe** is the clear winner.

## Implementation
Integration completed in 3 weeks. No issues in production. Processing $500K+ monthly.

**Author**: Alex Kumar  
**Date**: April 20, 2023  
**Status**: Implemented
"""
        })
        
        # Team Expertise Directory
        documents.append({
            "id": "DOC-001",
            "title": "Engineering Team Expertise Directory",
            "type": "Team Directory",
            "author": "david.thompson",
            "date": "2024-01-15",
            "folder": "Engineering/Team",
            "content": """# Engineering Team Expertise Directory

## Database & Infrastructure
- **Sarah Chen**: PostgreSQL, MySQL, Database Architecture, Python
- **Maria Garcia**: Kubernetes, CI/CD, Database Operations, AWS
- **Priya Patel**: Data Pipelines, PostgreSQL, ETL, Analytics

## Frontend
- **James Wilson**: React, System Architecture, Technical Strategy
- **Lisa Park**: React, TypeScript, UI/UX, Performance
- **Carlos Mendez**: Frontend Development, Vue, React

## Backend & APIs
- **Alex Kumar**: Payment Systems, API Design, Node.js, Stripe
- **Kevin Brown**: Backend Development, Java, Microservices
- **Jennifer Lee**: Backend Development, Python, APIs

## DevOps & Security
- **Maria Garcia**: Kubernetes, CI/CD, Infrastructure
- **Michael O'Connor**: Security, Compliance, GDPR, Penetration Testing
- **Daniel Martinez**: SRE, Monitoring, Observability

## Quality & Testing
- **Robert Zhang**: Test Automation, QA, Performance Testing
- **Ryan Jackson**: Data Analysis, Testing, Metrics

## Leadership
- **David Thompson**: Engineering Management, Microservices, System Design
- **Emily Rodriguez**: Product Management, Market Expansion, Strategy

Last Updated: January 15, 2024
"""
        })
        
        # Additional documents
        documents.extend([
            {
                "id": "DOC-120",
                "title": "Microservices Architecture Guide",
                "type": "Technical Guide",
                "author": "david.thompson",
                "date": "2022-08-20",
                "folder": "Engineering/Architecture",
                "content": "Guide to our microservices architecture including service boundaries, communication patterns, and deployment strategies."
            },
            {
                "id": "DOC-130",
                "title": "Database Best Practices",
                "type": "Best Practices",
                "author": "sarah.chen",
                "date": "2023-10-01",
                "folder": "Engineering/Best Practices",
                "content": "Best practices for database operations including connection pooling, indexing, query optimization, and migration strategies. Lessons learned from the PostgreSQL migration failure."
            },
            {
                "id": "DOC-140",
                "title": "Frontend Development Standards",
                "type": "Standards",
                "author": "james.wilson",
                "date": "2022-04-01",
                "folder": "Engineering/Standards",
                "content": "Standards for React development including component structure, state management, testing, and code style."
            }
        ])
        
        output_file = self.output_dir / "documents.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2)
        
        print(f"   ✓ Generated {len(documents)} documents")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = DemoDataGenerator()
    generator.generate_all()
