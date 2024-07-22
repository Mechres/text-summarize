
# Multilingual Text Summarization and Translation API

  

Flask-based API that provides a user-friendly interface to summarize text in any language supported by the BART model and then translate it to English.

  

## Features

  

*  **Summarization:** Employs Facebook's powerful BART-large-CNN model to condense text while retaining key information.
*  **Translation:** Automatically detects the source language and translates the summary to English using the Helsinki-NLP Opus-MT model.
*  **Simple Interface:** A clean web interface (`index.html`) for inputting text and receiving the summarized and translated output.
*  **API Endpoint:** A `/summarize` endpoint for seamless integration into other applications.

  

## Usage

1. Run the app:

>     python app.py

2. Open your web browser and navigate to http://127.0.0.1:5000/.

3. Paste your text into the input box and click "Summarize".

**API Endpoint:**
1. Send a POST request to `http://127.0.0.1:5000/summarize` with a JSON payload containing the `text` to be summarized.
2.  The API will return a JSON response with the `summary` and `detected_language`.
```
{
  "summary": "Translated summary of the text",
  "detected_language": "fr"  // Example: French
}
```


## Dependencies

-   Flask
-   Transformers (Hugging Face)
-   Langdetect

## Model Information

-   **Summarization:** Facebook BART-large-CNN
-   **Translation:** Helsinki-NLP Opus-MT

## Limitations

-   Summarization and translation quality can vary depending on the input text and language.
-   The models have specific language capabilities. If a language is unsupported, the summary will be in the original language without translation.

## Contribution

Feel free to submit issues and pull requests to improve this project!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
