from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect
import logging
from functools import lru_cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import torch
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Setup rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Setup models
device = "cuda" if torch.cuda.is_available() else "cpu"
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
translator = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-mul-en").to(device)
translator_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-mul-en")

# Thread pool for concurrent processing
executor = ThreadPoolExecutor(max_workers=4)

@lru_cache(maxsize=100)
def summarize_and_translate(text, target_lang="en", max_length=150, min_length=30):
    try:
        detected_lang = detect(text)

        # Step 1: Summarize
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

        # Step 2: Translate if not in English
        if detected_lang != "en" and target_lang == "en":
            inputs = translator_tokenizer(summary, return_tensors="pt")
            translated = translator.generate(**inputs)
            summary = translator_tokenizer.decode(translated[0], skip_special_tokens=True)

        return summary, detected_lang
    except Exception as e:
        logging.error(f"Error in summarize_and_translate: {str(e)}")
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
@limiter.limit("10 per minute")
def summarize():
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        max_length = data.get('max_length', 150)
        min_length = data.get('min_length', 30)

        summary, detected_lang = summarize_and_translate(text, "en", max_length, min_length)
        if summary is None:
            return jsonify({'error': 'Failed to process text'}), 500

        return jsonify({
            'summary': summary,
            'detected_language': detected_lang
        })
    except Exception as e:
        logging.error(f"Error in summarize route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)