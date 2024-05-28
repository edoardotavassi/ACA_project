# backend/__init__.py

from fastapi import FastAPI
from routes import router

app = FastAPI()

app.include_router(router)

@app.get("/", status_code=200)
def root():
    return {"ACA_PROJECT"}

@app.get("/health_check", status_code=200)
def health_check():
    return {"Status": "OK"}
