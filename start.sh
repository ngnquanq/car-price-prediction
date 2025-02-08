#!/bin/sh
# Start the Uvicorn server
uvicorn api.main:app --host 0.0.0.0 --port 80 &

# Wait for the server to start
sleep 5

# Use curl to check if the server is running
curl -s http://localhost:80 > /dev/null && echo "Server is running"

# Automatically open the browser
xdg-open http://localhost:80

# Keep the container running
tail -f /dev/null