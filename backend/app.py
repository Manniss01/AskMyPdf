from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.tutor_agent import get_tutor_response
from agents.memory_agent import save_session
from utils.document_loader import load_pdf_vectorstore
from utils.pdf_info import extract_pdf_info
import tempfile
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os

os.environ["HF_HOME"] = "D:/huggingface"

app = Flask(__name__)
CORS(app)

vectorstore = None
current_topics = []
current_summaries = {}

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    if not text.strip():
        text = "No extractable text found in PDF."
    return text

def extract_topics_tfidf(text, top_n=10):
    docs = [sentence.strip() for sentence in re.split(r'[.?!]\s*', text) if sentence.strip()]
    if not docs:
        return []

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.sum(axis=0).A1
    term_scores = list(zip(feature_names, scores))
    term_scores.sort(key=lambda x: x[1], reverse=True)

    topics = [term for term, score in term_scores[:top_n]]
    return topics

def extract_topic_summaries(text, topics, top_n_sentences=3):
    sentences = [s.strip() for s in re.split(r'[.?!]\s*', text) if s.strip()]
    if not sentences:
        return {topic: "No summary available." for topic in topics}

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(sentences)

    topic_summaries = {}
    for topic in topics:
        topic_vec = vectorizer.transform([topic])
        cosine_sim = (X * topic_vec.T).toarray().flatten()
        top_indices = cosine_sim.argsort()[-top_n_sentences:][::-1]
        top_sentences = [sentences[i] for i in top_indices if cosine_sim[i] > 0]

        if top_sentences:
            summary = ' '.join(top_sentences)
        else:
            summary = "No relevant content found."
        topic_summaries[topic] = summary
    return topic_summaries


def classify_pdf_content(text: str):
    categories = {
        "Science": {"experiment", "research", "data", "study", "method", "analysis"},
        "Business": {"market", "finance", "investment", "sales", "business", "strategy"},
        "CV": {"resume", "experience", "education", "skills", "profile", "employment"},
        "Research Paper": {"abstract", "introduction", "results", "conclusion", "methodology", "discussion"},
        "Law": {"court", "law", "contract", "legal", "judge", "litigation"},
        # Add more categories here as needed
    }

    text_lower = text.lower()
    scores = {cat: 0 for cat in categories}

    for cat, keywords in categories.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                scores[cat] += 1

    max_score = max(scores.values())
    if max_score == 0:
        return ["Unknown"]

    # Return all categories with the highest score
    return [cat for cat, score in scores.items() if score == max_score]

@app.route('/upload', methods=['POST'])
def upload():
    global vectorstore, current_topics, current_summaries
    try:
        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        pdf = request.files['pdf']
        if pdf.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.save(tmp.name)
            tmp_path = tmp.name

        try:
            vectorstore = load_pdf_vectorstore(tmp_path)

            raw_text = extract_text_from_pdf(tmp_path)
            current_topics = extract_topics_tfidf(raw_text, top_n=10)
            current_summaries = extract_topic_summaries(raw_text, current_topics)

            pdf_info = extract_pdf_info(tmp_path)
            classification = classify_pdf_content(raw_text)

            return jsonify({
                "message": "PDF processed successfully.",
                "topics": current_topics,
                "pdf_info": pdf_info,
                "classification": classification
            })
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    global vectorstore
    if vectorstore is None:
        return jsonify({"error": "Upload a PDF first to initialize the vectorstore"}), 400
    try:
        data = request.json
        question = data.get('question')
        session_id = data.get('session_id')
        if not question or not session_id:
            return jsonify({"error": "Missing question or session_id"}), 400

        answer = get_tutor_response(vectorstore, question)
        save_session(session_id, question, answer)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
