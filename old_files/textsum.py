from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect

"""
Takes the text in any language, summarizes it and translates to english.
bart-large-cnn is for summarizing the text.
opus-mt-mul-en is for translate the text to English.
"""

def setup_models():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    translator = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-mul-en")
    translator_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-mul-en")
    return summarizer, translator, translator_tokenizer

def summarize_and_translate(text, summarizer, translator, translator_tokenizer, target_lang="en"):
    detected_lang = detect(text)

    # Step 1: Summarize
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    # Step 2: Translate if not in English
    if detected_lang != "en" and target_lang == "en":
        inputs = translator_tokenizer(summary, return_tensors="pt")
        translated = translator.generate(**inputs)
        summary = translator_tokenizer.decode(translated[0], skip_special_tokens=True)
    return summary, detected_lang



summarizer, translator, translator_tokenizer = setup_models()

# Test texts
texts = {
    "English": """
    The Python programming language is widely used in data science, web development, and artificial intelligence. 
    It's known for its simplicity and readability, making it an excellent choice for beginners and experienced programmers alike. 
    Python's extensive library ecosystem, including popular packages like NumPy, Pandas, and TensorFlow, 
    contributes to its versatility and power in various domains.
    """,
    "Russian": """
    Язык программирования Python широко используется в науке о данных, веб-разработке и искусственном интеллекте.
    Он известен своей простотой и читаемостью, что делает его отличным выбором как для начинающих, так и для опытных программистов.
    Обширная экосистема библиотек Python, включая популярные пакеты, такие как NumPy, Pandas и TensorFlow,
    способствует его универсальности и мощности в различных областях.
    """,
    "Turkish": """
    Python programlama dili, veri bilimi, web geliştirme ve yapay zeka alanlarında yaygın olarak kullanılmaktadır.
    Basitliği ve okunabilirliği ile tanınan Python, hem yeni başlayanlar hem de deneyimli programcılar için mükemmel bir seçimdir.
    NumPy, Pandas ve TensorFlow gibi popüler paketleri içeren geniş kütüphane ekosistemi,
    çeşitli alanlarda çok yönlülüğüne ve gücüne katkıda bulunmaktadır.
    """
}

# Test the function for each language
for lang, text in texts.items():
    summary, detected_lang = summarize_and_translate(text, summarizer, translator, translator_tokenizer)
    print(f"\n{lang} summary (detected language: {detected_lang}):")
    print(summary)