from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect


"""
Takes the text in any language bart model supports, summarizes it and translates to english.
bart-large-cnn is for summarizing the text.
opus-mt-mul-en is for translate the text to English.
"""

app = Flask(__name__)

# Setup models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
translator = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-mul-en")
translator_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-mul-en")


def summarize_and_translate(text, target_lang="en"):
    detected_lang = detect(text)

    # Step 1: Summarize
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    # Step 2: Translate if not in English
    if detected_lang != "en" and target_lang == "en":
        inputs = translator_tokenizer(summary, return_tensors="pt")
        translated = translator.generate(**inputs)
        summary = translator_tokenizer.decode(translated[0], skip_special_tokens=True)

    return summary, detected_lang


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.json['text']
    summary, detected_lang = summarize_and_translate(text)
    return jsonify({
        'summary': summary,
        'detected_language': detected_lang
    })


if __name__ == '__main__':
    app.run(debug=True)