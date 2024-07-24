# Multilingual Text Summarization and Translation API
<div align="center">
  <img src="https://github.com/user-attachments/assets/c34b0edc-f2fe-4dc5-8c9f-5663dc84ec5e" width="200" height="200"/>
</div>

A Flask-based API that provides a user-friendly interface to summarize text in any language supported by the BART model and then translate it to English. This application offers both a web interface and an API endpoint for easy integration.

## Features

* **Summarization:** Employs Facebook's powerful BART-large-CNN model to condense text while retaining key information.
* **Translation:** Automatically detects the source language and translates the summary to English using the Helsinki-NLP Opus-MT model.
* **Simple Web Interface:** A clean, responsive web interface for inputting text and receiving the summarized and translated output.
* **API Endpoint:** A `/summarize` endpoint for seamless integration into other applications.
* **Configurable Summary Length:** Users can specify minimum and maximum lengths for the summary.
* **GPU Acceleration:** Utilizes CUDA if available for faster processing.
* **Rate Limiting:** Implements rate limiting to prevent API abuse.
* **Concurrent Processing:** Uses a ThreadPoolExecutor for handling multiple requests efficiently.
* **Health Check Endpoint:** Includes a `/health` endpoint for monitoring the application's status.

## Usage

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   python app.py
   ```

3. Open your web browser and navigate to `http://localhost:5000/`.

4. Enter your text, adjust the min and max length if desired, and click "Summarize".

### API Endpoint

Send a POST request to `http://localhost:5000/summarize` with a JSON payload:

```json
{
  "text": "Your long text here",
  "min_length": 30,
  "max_length": 150
}
```

The API will return a JSON response:

```json
{
  "summary": "Translated summary of the text",
  "detected_language": "fr"  // Example: French
}
```

## Dependencies

- Flask
- Transformers (Hugging Face)
- Langdetect
- PyTorch
- Flask-Limiter

## Model Information

- **Summarization:** Facebook BART-large-CNN
- **Translation:** Helsinki-NLP Opus-MT

## Limitations

- Summarization and translation quality can vary depending on the input text and language.
- The models have specific language capabilities. If a language is unsupported, the summary will be in the original language without translation.
- GPU acceleration requires a CUDA-compatible GPU.

## Configuration

- Adjust the rate limiting rules in `app.py` as needed.
- The application uses the `PORT` environment variable if set, otherwise defaults to port 5000.

## Deployment

The application is configured to run on `0.0.0.0` and can use a port specified by the `PORT` environment variable, making it suitable for deployment on various platforms.

## Contribution

Feel free to submit issues and pull requests to improve this project!

## License

This project is licensed under the MIT License - see the LICENSE file for details.