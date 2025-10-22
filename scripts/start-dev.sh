#!/bin/bash

# Start both frontend and backend in development mode
# This script uses tmux to run them in split panes

echo "🚀 Starting Faiz Lab in development mode..."

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux not found. Starting services sequentially instead."
    echo ""
    
    # Start backend in background
    echo "Starting backend..."
    cd backend/job-scraper
    source venv/bin/activate
    uvicorn app.main:app --reload --port 8001 &
    BACKEND_PID=$!
    cd ../..
    
    # Start frontend
    echo "Starting frontend..."
    cd web
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "✅ Services started!"
    echo "Frontend: http://localhost:3000"
    echo "Backend:  http://localhost:8001"
    echo "API Docs: http://localhost:8001/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Trap Ctrl+C to kill both processes
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    
    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
    
else
    # Use tmux for a better experience
    SESSION_NAME="faiz-lab"
    
    # Kill existing session if it exists
    tmux kill-session -t $SESSION_NAME 2>/dev/null
    
    # Create new session with backend
    tmux new-session -d -s $SESSION_NAME -n "services"
    
    # Split window horizontally
    tmux split-window -h -t $SESSION_NAME
    
    # Run backend in left pane
    tmux send-keys -t $SESSION_NAME:0.0 "cd backend/job-scraper && source venv/bin/activate && uvicorn app.main:app --reload --port 8001" C-m
    
    # Run frontend in right pane
    tmux send-keys -t $SESSION_NAME:0.1 "cd web && npm run dev" C-m
    
    # Attach to session
    echo "✅ Starting tmux session..."
    echo ""
    echo "Services:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend:  http://localhost:8001"
    echo "  - API Docs: http://localhost:8001/docs"
    echo ""
    echo "Tmux commands:"
    echo "  - Switch panes: Ctrl+b then arrow keys"
    echo "  - Detach: Ctrl+b then d"
    echo "  - Kill session: tmux kill-session -t $SESSION_NAME"
    echo ""
    
    sleep 2
    tmux attach-session -t $SESSION_NAME
fi

