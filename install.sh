#!/bin/bash

echo "==============================================="
echo "   InfinityInsight Installation Script"
echo "   AI-Powered Analytics Platform"
echo "==============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux/Mac
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}Warning: This script is designed for Linux/Mac. For Windows, use WSL or Docker Desktop.${NC}"
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Step 1: Checking prerequisites..."
echo "-----------------------------------"

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3.11+ is required but not installed.${NC}"
    echo "Please install Python 3.11 or higher from https://www.python.org/"
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${YELLOW}! Node.js not found. Installing via nvm...${NC}"
fi

# Check Docker
if command_exists docker; then
    echo -e "${GREEN}✓ Docker found${NC}"
    USE_DOCKER="yes"
else
    echo -e "${YELLOW}! Docker not found. Will use local installation.${NC}"
    USE_DOCKER="no"
fi

# Check PostgreSQL
if command_exists psql; then
    echo -e "${GREEN}✓ PostgreSQL found${NC}"
else
    echo -e "${YELLOW}! PostgreSQL not found. Will use Docker or SQLite.${NC}"
fi

echo ""
echo "Step 2: Choose installation method"
echo "-----------------------------------"
echo "1) Docker (Recommended - Easy one-click deployment)"
echo "2) Local (Manual setup - More control)"
echo ""
read -p "Enter your choice (1 or 2): " INSTALL_METHOD

if [ "$INSTALL_METHOD" == "1" ]; then
    if [ "$USE_DOCKER" == "no" ]; then
        echo -e "${RED}Docker is required for this method. Please install Docker first.${NC}"
        exit 1
    fi

    echo ""
    echo "Starting Docker installation..."
    echo "-----------------------------------"

    # Create .env file from example
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
    fi

    # Build and run with Docker Compose
    echo "Building Docker containers..."
    docker-compose build

    echo "Starting services..."
    docker-compose up -d

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   Installation Complete! 🎉${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Services are now running:"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Frontend: http://localhost:3000"
    echo ""
    echo "To stop services: docker-compose down"
    echo "To view logs: docker-compose logs -f"
    echo ""

else
    echo ""
    echo "Starting local installation..."
    echo "-----------------------------------"

    # Create virtual environment
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate

    # Install Python dependencies
    echo "Installing Python dependencies (this may take a few minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt

    # Create .env file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${YELLOW}! Please edit .env file with your configuration${NC}"
    fi

    # Create directories
    mkdir -p data/uploads data/temp models logs

    # Setup database
    echo ""
    echo "Database setup:"
    read -p "Do you have PostgreSQL running? (y/n): " HAS_POSTGRES

    if [ "$HAS_POSTGRES" != "y" ]; then
        echo -e "${YELLOW}Please install and start PostgreSQL, or use SQLite by updating DATABASE_URL in .env${NC}"
        echo "Example SQLite: DATABASE_URL=sqlite:///./infinityinsight.db"
    fi

    # Install frontend dependencies
    if [ -d "frontend" ]; then
        echo ""
        echo "Installing frontend dependencies..."
        cd frontend
        if command_exists npm; then
            npm install
        else
            echo -e "${YELLOW}npm not found. Please install Node.js to build the frontend.${NC}"
        fi
        cd ..
    fi

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   Installation Complete! 🎉${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "To start the application:"
    echo ""
    echo "1. Activate virtual environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Start backend:"
    echo "   python -m uvicorn backend.app.main:app --reload"
    echo ""
    echo "3. Start frontend (in another terminal):"
    echo "   cd frontend && npm run dev"
    echo ""
    echo "Then access:"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Frontend: http://localhost:3000"
    echo ""
fi

echo "For more information, see README.md or CLAUDE.md"
echo ""
