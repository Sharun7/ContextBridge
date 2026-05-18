#!/bin/bash
set -e

echo "🚀 Starting ContextBridge build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p data/chroma_db
mkdir -p logs

# Initialize database
echo "🗄️ Initializing database..."
python -c "
from db.database import init_db
try:
    init_db()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️ Database initialization warning: {e}')
"

echo "✅ Build complete!"
