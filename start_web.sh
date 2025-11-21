#!/bin/bash

# Script to start the web frontend
# This script starts a simple web server for the frontend

echo "🌐 Starting Nutrition App Web Frontend..."
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3 to run the web server"
    exit 1
fi

# Navigate to web directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEB_DIR="$SCRIPT_DIR/web"

if [ ! -d "$WEB_DIR" ]; then
    echo "❌ Error: Web directory not found at $WEB_DIR"
    exit 1
fi

cd "$WEB_DIR"

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Warning: Backend doesn't seem to be running"
    echo "   Please start the backend first:"
    echo "   cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Find an available port
PORT=8080
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    echo "⚠️  Port $PORT is already in use, trying $((PORT+1))..."
    PORT=$((PORT+1))
done

echo ""
echo "🚀 Starting web server on port $PORT..."
echo "📂 Serving from: $WEB_DIR"
echo ""
echo "✅ Web app will be available at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try to open browser (optional)
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:$PORT" 2>/dev/null &
elif command -v open &> /dev/null; then
    open "http://localhost:$PORT" 2>/dev/null &
fi

# Start the web server
$PYTHON_CMD -m http.server $PORT

