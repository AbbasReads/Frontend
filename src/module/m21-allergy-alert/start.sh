#!/bin/bash

# Module 21: Allergy-Aware Medication Alert System (Python/MongoDB)
# Quick start script

echo "🏥 Starting M21 Allergy Alert System (Python/MongoDB)..."

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "❌ MongoDB is not running. Please start MongoDB first:"
    echo "   macOS: brew services start mongodb-community"
    echo "   Linux: sudo systemctl start mongod"
    echo "   Windows: Start MongoDB service"
    exit 1
fi

# Check if Python dependencies are installed
if ! python -c "import streamlit, fastapi, pymongo" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    python setup.py
fi

# Start FastAPI backend in background
echo "🚀 Starting FastAPI backend..."
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend..."
cd ../frontend
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "✅ M21 Allergy Alert System is now running!"
echo ""
echo "🔗 Streamlit Dashboard: http://localhost:8501"
echo "🔗 FastAPI Backend: http://localhost:8000"
echo "🔗 API Documentation: http://localhost:8000/docs"
echo "🔗 MongoDB Database: m21_allergy_alert"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait