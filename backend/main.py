# backend/main.py

import uvicorn
from __init__ import app

def run_server():
    """
    Runs the server using the specified host and port.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == '__main__':
    run_server()
