import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()  # definition of framework


# name of the app framework
@app.get("/", status_code=200)
def root():
    return {"ACA_PROJECT"}

# health check that return the status with 200 code
@app.get("/health_check", status_code=200)
def health_check():
    return {"Status": "OK"}


# if the user insert an empty string we handle this situation as an exception
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status": "Error"}),
    )



class SyntetizeRequest(BaseModel):
    text: str
    language: str

@app.post("/synthetize")
async def synthetize(request: SyntetizeRequest):
    return{
        "text": request.text,
        "language": request.language,
        "message": "Data received succesfully"
    }



# classic main method
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5555)