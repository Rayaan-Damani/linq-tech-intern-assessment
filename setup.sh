#!/bin/bash

# Linq Assessment Setup Script
# This script helps set up the entire project

echo "🚀 Linq Technology Intern Assessment Setup"
echo "=========================================="

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker and Docker Compose are installed"
    
    echo ""
    echo "Starting Docker containers..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Waiting for MongoDB to be ready..."
    sleep 10
    
    echo ""
    echo "📊 Running database setup..."
    docker exec linq-python python datastore_setup.py
    
    echo ""
    echo "💾 Ingesting sample data..."
    docker exec linq-python python data_ingest.py --records 2000 --days 30
    
    echo ""
    echo "🔄 Running data transformations..."
    docker exec linq-python python transformations.py
    
    echo ""
    echo "✨ Setup complete!"
    echo ""
    echo "📊 Access Grafana at: http://localhost:3000"
    echo "   Username: admin"
    echo "   Password: admin"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Take a screenshot of the Grafana dashboard"
    echo "   2. Save it as 'dashboard.png' in the project root"
    echo "   3. Review all generated files"
    echo "   4. Push to GitHub and submit!"
    
else
    echo "⚠️  Docker not found. Running manual setup..."
    echo ""
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    
    echo ""
    echo "Please ensure MongoDB is running locally, then run:"
    echo "  python datastore_setup.py"
    echo "  python data_ingest.py"
    echo "  python transformations.py"
fi