from fastapi import FastAPI
import models
from database import engine
from routes import smoke_detect

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(smoke_detect.router)
