#!/bin/bash
# Simple test script to check backend startup

echo "Testing FloxAI backend startup..."

# Check if we're in Flox environment
if [ -z "$FLOX_ENV" ]; then
    echo "❌ Not in Flox environment"
    exit 1
fi

echo "✅ In Flox environment: $FLOX_ENV_NAME"

# Check Python
echo "🐍 Python version: $(python --version)"

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found"
    exit 1
fi

echo "✅ Backend directory found"

# Check if main.py exists
if [ ! -f "backend/app/main.py" ]; then
    echo "❌ main.py not found"
    exit 1
fi

echo "✅ main.py found"

# Try to start backend
echo "🚀 Starting backend..."
cd backend
python app/main.py &
BACKEND_PID=$!

# Wait a moment
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on port 8000"
    kill $BACKEND_PID
    echo "✅ Test successful - backend can start"
else
    echo "❌ Backend failed to start"
    echo "Backend process status:"
    ps aux | grep python | grep main.py || echo "No backend process found"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi
