from fastapi import FastAPI
import models
from database import engine
from routes import smoke_detect
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify specific methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # Allow all headers, or specify specific headers
)
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
app.include_router(smoke_detect.router)
