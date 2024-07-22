from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import os

"""This doesn't work! I'll look into this when i have more time."""

model_name = "google/mt5-small"
cache_dir = "./model_cache"

# Ensure the cache directory exists
os.makedirs(cache_dir, exist_ok=True)

# Force download (I had a problem downloading, had to use force download)
tokenizer = MT5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir, force_download=False)
model = MT5ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir, force_download=False)

def summarize_text(text, max_length=150):
    # Add the task prefix
    input_text = "summarize: " + text
    
    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate summary
    summary_ids = model.generate(
        inputs.input_ids, 
        num_beams=16,
        max_length=max_length, 
        min_length=30, 
        length_penalty=2.0,
        early_stopping=True
    )
    
    # Decode and return the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Test the function
test_text = """
The Python programming language is widely used in data science, web development, and artificial intelligence. 
It's known for its simplicity and readability, making it an excellent choice for beginners and experienced programmers alike. 
Python's extensive library ecosystem, including popular packages like NumPy, Pandas, and TensorFlow, 
contributes to its versatility and power in various domains.
"""

print(summarize_text(test_text))