# backend/main.py

import uvicorn
from __init__ import app

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
