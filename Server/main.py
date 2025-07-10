from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
from huggingface_hub import InferenceClient

# Set path for pytesseract if using macOS (M1/M2)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Hugging Face model setup
HF_TOKEN = "your_huggingface_token_here"
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Confidence estimation from AI response
def estimate_confidence(ai_response: str) -> int:
    response = ai_response.lower()
    if "definitely" in response or "clearly" in response:
        return 95
    elif "appears to be" in response or "seems like" in response:
        return 80
    elif "could be" in response or "might be" in response:
        return 65
    elif "uncertain" in response or "manual review needed" in response:
        return 40
    else:
        return 50

# Main API route
@app.post("/validate-doc")
async def validate_doc(file: UploadFile = File(...)):
    try:
        # Read uploaded image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # OCR extract text from image
        extracted_text = pytesseract.image_to_string(image)

        # Prepare prompt for AI
        user_prompt = f"""
        You are a real estate document validator AI.

        OCR Extracted Text:
        {extracted_text}

        Based on the above text, answer:
        1. What type of document is this? (e.g., PAN Card, EC, Tax Receipt)
        2. Is this document valid or fake?
        3. A short reason for your decision.
        """

        # Get AI response from Hugging Face
        response = client.text_generation(
            prompt=user_prompt,
            max_new_tokens=300,
            temperature=0.7,
        )

        confidence = estimate_confidence(response)

        return JSONResponse({
            "document_text": extracted_text[:1000],
            "ai_verdict": response.strip(),
            "confidence_score": confidence
        })

    except Exception as e:
        print("Error occurred:", e)  # print full traceback in terminal
        return JSONResponse(status_code=500, content={"error": str(e)})
