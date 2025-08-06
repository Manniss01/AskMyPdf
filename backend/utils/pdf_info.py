import PyPDF2
from transformers import pipeline
import os
import os

# Set custom cache directory on D: drive
os.environ["HF_HOME"] = "D:/huggingface"

# Disable symlink warnings if symlinks are not supported
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"





def get_summarizer():
    try:
        # Load summarizer (can be optimized with caching in production)
        return pipeline("summarization",)
    except Exception as e:
        print(f"Summarizer loading failed: {e}")
        return None

summarizer = get_summarizer()

def extract_pdf_info(file_stream):
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        num_words = len(text.split())
        num_pages = len(reader.pages)
        pdf_type = "Text-based" if text.strip() else "Scanned (image-based)"

        if summarizer and text:
            summary = summarizer(text[:1000], max_length=100, min_length=25, do_sample=False)[0]['summary_text']
        else:
            summary = "Summary unavailable due to model load failure or empty text."

        return {
            "pages": num_pages,
            "words": num_words,
            "summary": summary,
            "pdf_type": pdf_type
        }

    except Exception as e:
        return {"error": str(e)}