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
    """
    Returns the root endpoint of the ACA_PROJECT backend.
    """
    return {"ACA_PROJECT"}

@app.get("/health_check", status_code=200)
def health_check():
    """
    Endpoint for health check.

    Returns:
        dict: A dictionary with the status "OK".
    """
    return {"Status": "OK"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Exception handler for RequestValidationError.

    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The raised RequestValidationError.

    Returns:
        JSONResponse: A JSON response with a status code of 500 and an error message.
    """
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status": "Error"}),
    )