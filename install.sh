#!/bin/bash

# =============================================================================
# InfinityInsight - Super Simple Installation Script
# =============================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║         ${GREEN}InfinityInsight Installation Wizard${BLUE}           ║${NC}"
echo -e "${BLUE}║         ${YELLOW}AI-Powered Analytics Platform${BLUE}                ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    HAS_DOCKER=true
    echo -e "${GREEN}✓ Docker detected${NC}"
else
    HAS_DOCKER=false
    echo -e "${YELLOW}! Docker not found - will use local installation${NC}"
fi

echo ""
echo "Choose installation method:"
echo ""
echo -e "${GREEN}1) Docker (Recommended)${NC} - Everything in containers, zero config needed"
echo -e "${BLUE}2) Local${NC} - Install on your machine directly"
echo ""

read -p "Enter your choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    if [ "$HAS_DOCKER" = false ]; then
        echo ""
        echo -e "${RED}❌ Docker is not installed!${NC}"
        echo ""
        echo "Please install Docker first:"
        echo "  - macOS: https://docs.docker.com/desktop/mac/install/"
        echo "  - Windows: https://docs.docker.com/desktop/windows/install/"
        echo "  - Linux: https://docs.docker.com/engine/install/"
        echo ""
        exit 1
    fi

    echo ""
    echo -e "${GREEN}Starting Docker installation...${NC}"
    echo ""

    # Stop and remove existing containers
    echo "Cleaning up old containers..."
    docker-compose down 2>/dev/null || true

    # Build and start
    echo "Building containers (this may take a few minutes)..."
    docker-compose up -d --build

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║              ✓ Installation Complete! 🎉                  ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Services are running at:${NC}"
    echo ""
    echo -e "  ${GREEN}➜${NC} Backend API:      http://localhost:8000"
    echo -e "  ${GREEN}➜${NC} API Documentation: http://localhost:8000/docs"
    echo -e "  ${GREEN}➜${NC} Frontend:         http://localhost:3000"
    echo ""
    echo -e "${YELLOW}Useful commands:${NC}"
    echo "  docker-compose logs -f     # View logs"
    echo "  docker-compose down        # Stop services"
    echo "  docker-compose up -d       # Start services"
    echo ""

elif [ "$choice" == "2" ]; then
    echo ""
    echo -e "${GREEN}Starting local installation...${NC}"
    echo ""

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found!${NC}"
        echo "Please install Python 3.11+ from https://www.python.org/"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}! Node.js not found - frontend won't be built${NC}"
        HAS_NODE=false
    else
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
        HAS_NODE=true
    fi

    # Create virtual environment
    echo ""
    echo "Creating Python virtual environment..."
    python3 -m venv venv

    # Activate venv
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip --quiet

    # Install Python dependencies
    echo "Installing Python dependencies (this may take a few minutes)..."
    pip install -r requirements.txt --quiet

    echo -e "${GREEN}✓ Backend dependencies installed${NC}"

    # Create directories
    mkdir -p data/uploads data/temp models logs

    # Check if .env exists
    if [ ! -f .env ]; then
        echo ""
        echo -e "${YELLOW}Creating .env file...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo -e "${YELLOW}Note: Using SQLite database for easy setup${NC}"
    fi

    # Install frontend dependencies
    if [ "$HAS_NODE" = true ] && [ -d "frontend" ]; then
        echo ""
        echo "Installing frontend dependencies..."
        cd frontend
        npm install --quiet
        cd ..
        echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    fi

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║              ✓ Installation Complete! 🎉                  ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}To start the application:${NC}"
    echo ""
    echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
    echo "  source venv/bin/activate"
    echo "  python -m uvicorn backend.app.main:app --reload"
    echo ""

    if [ "$HAS_NODE" = true ]; then
        echo -e "${YELLOW}Terminal 2 - Frontend:${NC}"
        echo "  cd frontend"
        echo "  npm run dev"
        echo ""
    fi

    echo -e "${BLUE}Then access:${NC}"
    echo "  Backend:  http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    if [ "$HAS_NODE" = true ]; then
        echo "  Frontend: http://localhost:3000"
    fi
    echo ""

else
    echo ""
    echo -e "${RED}Invalid choice. Please run again and choose 1 or 2.${NC}"
    exit 1
fi

echo -e "${GREEN}Happy analyzing! 📊${NC}"
echo ""
