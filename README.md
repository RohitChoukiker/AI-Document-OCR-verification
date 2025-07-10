# AI-Document Verification System

An AI-powered document validator that uses OCR and Hugging Face language models to identify and validate scanned property-related documents like PAN cards, Encumbrance Certificates, Tax Receipts, and more.

> 📌 Built using FastAPI, Tesseract OCR, and Hugging Face's Zephyr LLM.

---

## 🚀 Features

- 🧾 Accepts scanned real estate documents (images)
- 🧠 Extracts text using Tesseract OCR
- 🤖 Uses Hugging Face LLM to:
  - Detect document type (e.g., PAN Card, EC, etc.)
  - Determine validity (Valid / Invalid)
  - Provide reasoning
- 📊 Returns AI confidence score (%)
- ⚙️ REST API with clean JSON output
- 🔐 Built for future extensions: PDF support, DB logging, etc.

---

## 🧰 Tech Stack

| Layer         | Tools                                |
|---------------|---------------------------------------|
| OCR           | Tesseract OCR                         |
| AI Model      | HuggingFaceH4/zephyr-7b-beta          |
| Backend       | FastAPI                               |
| Language      | Python 🐍                             |
| Extras        | HuggingFace Hub, PIL, CORS middleware |

---

## 🛠️ Setup Instructions (Mac/Linux)

### 1. Clone the Repository
```bash
git clone https://github.com/RohitChoukiker/AI-Document-OCR-verification.git
cd AI-Document-OCR-verification
