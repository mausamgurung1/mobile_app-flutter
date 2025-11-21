#!/bin/bash

# Backend Server Startup Script
# Run this in a separate terminal to see backend logs

echo "🚀 Starting Backend API Server..."
echo "=================================="
echo ""

cd "/home/mausamgr/flutter /backend"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install email-validator
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
DATABASE_URL=sqlite:///./nutrition.db
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars-long-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
fi

echo ""
echo "✅ Backend starting..."
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔗 API Base URL: http://localhost:8000/api/v1"
echo "💚 Health Check: http://localhost:8000/health"
echo "📱 Accessible from Android emulator: http://10.0.2.2:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

