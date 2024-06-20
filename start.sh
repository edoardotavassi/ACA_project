#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Start the backend server in the background
echo "Starting backend server..."
python -m backend.main &

# Save the backend PID
BACKEND_PID=$!

# Give the backend server a few seconds to start
sleep 5

# Start the frontend interface
echo "Starting frontend interface..."
streamlit run ui/main.py &

# Save the frontend PID
FRONTEND_PID=$!

# Write the PIDs to a file
echo $BACKEND_PID > pids.txt
echo $FRONTEND_PID >> pids.txt

# Keep the script running
wait