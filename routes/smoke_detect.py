from fastapi import APIRouter, File, UploadFile, HTTPException
from starlette import status
from cnnClassifier.pipeline.predict import PredictionPipeline


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline()


router = APIRouter()
clApp = ClientApp()


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

