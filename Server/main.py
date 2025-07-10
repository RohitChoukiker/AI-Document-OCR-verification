from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
from huggingface_hub import InferenceClient


HF_TOKEN = "your_huggingface_token_here"  
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"

client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/validate-doc")
async def validate_doc(file: UploadFile = File(...)):
    try:
       
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        
        extracted_text = pytesseract.image_to_string(image)

       
        prompt = f"""
        You are a real estate document validator AI.

        Analyze the OCR extracted text below and identify:
        1. The document type (e.g., PAN Card, EC Certificate, Tax Receipt)
        2. Whether it is valid or invalid
        3. A short reason explaining the validation

        OCR Text:
        {extracted_text}
        """

        
        response = client.text_generation(
            prompt,
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
        return JSONResponse(status_code=500, content={"error": str(e)})
