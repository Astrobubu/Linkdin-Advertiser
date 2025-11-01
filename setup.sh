#!/bin/bash

echo "🔧 LinkedIn Advertiser - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Check Node version
echo ""
echo "2️⃣  Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js version: $NODE_VERSION"

# Setup Backend
echo ""
echo "3️⃣  Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "   Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "   Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "   Installing Playwright browsers..."
playwright install chromium

# Initialize database
echo "   Initializing database..."
python -c "from database import init_db; init_db()"

cd ..

# Setup Frontend
echo ""
echo "4️⃣  Setting up frontend..."
cd frontend

# Install npm dependencies
echo "   Installing npm dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Verify your OpenAI API key in .env file"
echo "   2. Run './run.sh' to start both servers"
echo "   3. Open http://localhost:3000 in your browser"
echo ""
