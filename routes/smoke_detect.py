from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request, Response
from starlette import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cnnClassifier.pipeline.predict import PredictionPipeline


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline()


router = APIRouter()
clApp = ClientApp()
templates = Jinja2Templates(directory="templates")


@router.get("/", status_code=status.HTTP_200_OK)
async def home(request: Request):
    return {"message" : "API is Running"}


@router.post("/smoke_detection_url")
async def detect_smoke_from_url(url: str = Form(...)):
    try:
        # Validate URL (you may want to use a more robust URL validation method)
        if not url.startswith("http"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")

        # Download image
        image_bytes = clApp.classifier.download_image(url)

        # Preprocess and predict
        img = clApp.classifier.preprocess_image(image_bytes)
        classification = clApp.classifier.predict(img)

        return classification

    except Exception as e:
        # Handle exceptions and return an appropriate HTTP response
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")


@router.post("/smoke_detection_img")
async def detect_smoke_from_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = clApp.classifier.preprocess_image(image_bytes)
    classification = clApp.classifier.predict(img)
    return classification

