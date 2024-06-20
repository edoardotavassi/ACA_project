#!/bin/bash

# Check if the pids.txt file exists
if [ -f pids.txt ]; then
  # Read the PIDs from the file
  PIDS=$(cat pids.txt)
  
  # Stop the processes
  echo "Stopping processes..."
  for PID in $PIDS; do
    kill $PID
  done

  # Remove the PIDs file
  rm pids.txt

  echo "Processes stopped."
else
  echo "No running processes found."
fi