from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.api import protected
from app.api import test_engine
from app.api import calculate

# Main FastAPI application instance
app = FastAPI(
    title="SmartCalc API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(test_engine.router)
app.include_router(calculate.router)


@app.get("/")
def root():
    return {
        "message": "SmartCalc API is running"
    }