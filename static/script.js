document.addEventListener('DOMContentLoaded', function() {
    const summarizeBtn = document.getElementById('summarize-btn');
    const inputText = document.getElementById('input-text');
    const summaryText = document.getElementById('summary-text');
    const detectedLanguage = document.getElementById('detected-language');
    const minLength = document.getElementById('min-length');
    const maxLength = document.getElementById('max-length');

    summarizeBtn.addEventListener('click', function() {
        const text = inputText.value;
        if (text.trim() === '') {
            alert('Please enter some text to summarize.');
            return;
        }

        const min = parseInt(minLength.value);
        const max = parseInt(maxLength.value);

        if (min >= max) {
            alert('Minimum length must be less than maximum length.');
            return;
        }

        summarizeBtn.disabled = true;
        summarizeBtn.textContent = 'Summarizing...';

        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                min_length: min,
                max_length: max
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            summaryText.textContent = data.summary;
            detectedLanguage.textContent = `Detected Language: ${data.detected_language}`;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while summarizing the text.');
        })
        .finally(() => {
            summarizeBtn.disabled = false;
            summarizeBtn.textContent = 'Summarize';
        });
    });
});