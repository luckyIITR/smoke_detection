from fastapi import FastAPI
import models
from database import engine
from routes import smoke_detect
from starlette.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
app.include_router(smoke_detect.router)
