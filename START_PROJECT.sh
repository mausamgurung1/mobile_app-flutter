#!/bin/bash

# Nutrition App - Start Script
# This script helps you start both backend and Flutter app

echo "🍎 Nutrition App - Startup Script"
echo "================================"
echo ""

# Check disk space
echo "📊 Checking disk space..."
AVAILABLE=$(df -h ~ | tail -1 | awk '{print $4}')
echo "Available space: $AVAILABLE"
echo ""

# Function to start backend
start_backend() {
    echo "🚀 Starting Backend Server..."
    cd ~/Desktop/flutter\ /backend
    
    # Check if venv exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Check if dependencies are installed
    if ! python3 -c "import fastapi" 2>/dev/null; then
        echo "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
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
    
    echo "✅ Backend starting on http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    uvicorn main:app --reload
}

# Function to start Flutter app
start_flutter() {
    echo "📱 Starting Flutter App..."
    cd ~/Desktop/flutter\ /mobile_app
    
    # Check if dependencies are installed
    if [ ! -d ".dart_tool" ]; then
        echo "Installing Flutter dependencies..."
        flutter pub get
    fi
    
    echo "✅ Flutter app starting..."
    echo ""
    
    # List available devices
    echo "Available devices:"
    flutter devices
    
    echo ""
    echo "Starting on macOS (change device as needed)..."
    flutter run -d macos
}

# Main menu
echo "What would you like to start?"
echo "1) Backend only"
echo "2) Flutter app only"
echo "3) Both (in separate terminals)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        start_backend
        ;;
    2)
        start_flutter
        ;;
    3)
        echo ""
        echo "⚠️  To run both, open TWO terminal windows:"
        echo ""
        echo "Terminal 1 - Backend:"
        echo "  cd ~/Desktop/flutter\ /backend"
        echo "  source venv/bin/activate"
        echo "  uvicorn main:app --reload"
        echo ""
        echo "Terminal 2 - Flutter:"
        echo "  cd ~/Desktop/flutter\ /mobile_app"
        echo "  flutter run -d macos"
        echo ""
        echo "Or run this script twice with options 1 and 2"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

