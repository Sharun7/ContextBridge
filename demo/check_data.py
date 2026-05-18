import json
from pathlib import Path

files = {
    'people.json': 'employees',
    'slack_messages.json': 'messages',
    'jira_tickets.json': 'tickets',
    'documents.json': 'documents'
}

print('\n📊 Demo Data Summary')
print('=' * 50)

for filename, label in files.items():
    filepath = Path('demo/data') / filename
    with open(filepath) as f:
        data = json.load(f)
    print(f'\n✓ {filename}:')
    print(f'  {len(data)} {label}')

print('\n' + '=' * 50)
print('✅ All demo data files generated successfully!\n')
