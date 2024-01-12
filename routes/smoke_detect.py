from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Response
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


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@router.get("/aboutme", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("aboutme.html", {"request": request})


@router.get("/smoke_detection/", status_code=status.HTTP_200_OK)
async def detect_smoke_from_url(url: str):
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


@router.post("/smoke_detection")
async def detect_smoke_from_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = clApp.classifier.preprocess_image(image_bytes)
    classification = clApp.classifier.predict(img)
    return classification
