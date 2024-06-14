# backend/__init__.py

from fastapi import FastAPI
from routes import router

from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()

app.include_router(router)

@app.get("/", status_code=200)
def root():
    return {"ACA_PROJECT"}

@app.get("/health_check", status_code=200)
def health_check():
    return {"Status": "OK"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status": "Error"}),
    )