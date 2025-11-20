#!/bin/bash

# Start Both Backend and Flutter App
# This script starts both services simultaneously

echo "🚀 Starting Nutrition App - Backend + Flutter"
echo "=============================================="
echo ""

# Function to start backend
start_backend() {
    echo "🔧 Starting Backend API..."
    cd ~/Desktop/flutter\ /backend
    
    # Check if already running
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend already running on http://localhost:8000"
        return 0
    fi
    
    # Activate venv and start
    source venv/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "Backend started (PID: $BACKEND_PID)"
    
    # Wait for backend to be ready
    echo "Waiting for backend to start..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend is running on http://localhost:8000"
            echo "📚 API Docs: http://localhost:8000/docs"
            return 0
        fi
        sleep 1
    done
    
    echo "❌ Backend failed to start. Check /tmp/backend.log"
    return 1
}

# Function to start Flutter
start_flutter() {
    echo ""
    echo "📱 Starting Flutter App..."
    cd ~/Desktop/flutter\ /mobile_app
    
    # Check if Flutter is already running
    if ps aux | grep -i "flutter run" | grep -v grep > /dev/null; then
        echo "✅ Flutter app already running"
        return 0
    fi
    
    # Start Flutter
    flutter run -d macos > /tmp/flutter.log 2>&1 &
    FLUTTER_PID=$!
    echo "Flutter started (PID: $FLUTTER_PID)"
    echo "✅ Flutter app is starting..."
    echo "   Check your screen for the app window"
    
    return 0
}

# Start both services
start_backend
start_flutter

echo ""
echo "=============================================="
echo "🎉 Both services are starting!"
echo ""
echo "Backend API: http://localhost:8000/docs"
echo "Flutter App: Check your screen"
echo ""
echo "To view logs:"
echo "  Backend: tail -f /tmp/backend.log"
echo "  Flutter: tail -f /tmp/flutter.log"
echo ""
echo "To stop:"
echo "  pkill -f 'uvicorn main:app'  # Stop backend"
echo "  pkill -f 'flutter run'       # Stop Flutter"
echo ""

