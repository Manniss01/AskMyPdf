# 🧠 AskMyPDF

**AskMyPDF** is an AI-powered PDF assistant that intelligently extracts content, summarizes it, detects key topics, classifies the document, and allows users to ask context-aware questions—all through an interactive and modern UI.

---

## ✨ Features

- 📄 Extracts text, word count, page count, and detects if it's scanned or text-based
- 📌 Detects key topics using TF-IDF
- 🧠 Summarizes content with HuggingFace Transformers
- ❓ Ask context-aware questions using OpenAI GPT
- 🗂️ Classifies PDF content (e.g., CV, Research, Law, etc.)
- 💾 Stores session Q&A history
- ⚡ Sleek React + TypeScript frontend

---

## 🧰 Tech Stack

**Frontend:**
- React + TypeScript
- CSS Modules

**Backend:**
- Flask + Flask-CORS (REST API)
- LangChain + FAISS (Vector Store)
- HuggingFace Transformers (Summarization)
- OpenAI GPT (Conversational Q&A)
- PyPDF2, pdfplumber (PDF Parsing)

---

## 🔌 APIs Used

| API Type         | Source           | Purpose                         |
|------------------|------------------|---------------------------------|
| REST             | Flask            | File upload, Q&A interaction    |
| OpenAI API       | Cloud            | Chat-based question answering   |
| Transformers API | Local (cached)   | Summarization using models      |
| LangChain + FAISS| Local            | Document vector storage & retrieval |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Manniss01/AskMyPdf.git
cd AskMyPDF
```

```bash
 Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Create a .env file in backend/

OPENAI_API_KEY=your_openai_api_key_here

python app.py

```
```bash
 Frontend Setup

cd frontend
npm install
npm run dev
```
The frontend will be available at: http://localhost:5173\

## 💡 Future Improvements

- 🔍 Page-specific Q&A
- 🔐 User login & session dashboard
- ☁️ Deploy on Hugging Face Spaces or Render
- 🎙️ Voice-based interaction



