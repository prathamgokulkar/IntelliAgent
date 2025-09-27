#!/bin/bash

# Start backend server
echo "🚀 Starting backend server..."
cd backend && npm start &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
cd ../server && npm run dev &
FRONTEND_PID=$!

# Function to cleanup processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "✅ Both servers are running!"
echo "📄 Backend API: http://localhost:3001"
echo "🎨 Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for processes
wait
