document.addEventListener('DOMContentLoaded', function() {
    const summarizeBtn = document.getElementById('summarize-btn');
    const inputText = document.getElementById('input-text');
    const summaryText = document.getElementById('summary-text');
    const detectedLanguage = document.getElementById('detected-language');

    summarizeBtn.addEventListener('click', function() {
        const text = inputText.value;
        if (text.trim() === '') {
            alert('Please enter some text to summarize.');
            return;
        }

        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.json())
        .then(data => {
            summaryText.textContent = data.summary;
            detectedLanguage.textContent = `Detected Language: ${data.detected_language}`;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while summarizing the text.');
        });
    });
});