document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('youtube-form');
    const resultContainer = document.getElementById('result-container');
    const statusMessage = document.getElementById('status-message');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Backend API URL - Updated to point to your Heroku backend
    const API_URL = 'https://youtube-to-text-backend-77ca40ac4b99.herokuapp.com/api/convert';

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const youtubeUrl = document.getElementById('youtube-url').value.trim();

        // Validate YouTube URL
        if (!isValidYoutubeUrl(youtubeUrl)) {
            alert('Please enter a valid YouTube URL');
            return;
        }

        // Show result container with loading state
        resultContainer.classList.remove('hidden');
        statusMessage.textContent = 'Processing your request. This may take a few minutes...';
        loadingSpinner.style.display = 'block';

        try {
            // Send request to backend
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ youtube_url: youtubeUrl })
            });

            const data = await response.json();

            if (data.success) {
                statusMessage.replaceChildren(
                    createParagraph('Transcription complete!'),
                    createTranscriptionResult(data.text || '')
                );
            } else {
                statusMessage.replaceChildren(createParagraph(`Error: ${data.error || 'Unknown error'}`));
            }
        } catch (error) {
            statusMessage.replaceChildren(
                createParagraph('Error: Could not connect to the server. Please try again later.'),
                createParagraph(`Details: ${error.message}`)
            );
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    function createParagraph(text) {
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        return paragraph;
    }

    function createTranscriptionResult(text) {
        const wrapper = document.createElement('div');
        wrapper.className = 'transcription-result';

        const heading = document.createElement('h3');
        heading.textContent = 'Transcribed Text:';

        const pre = document.createElement('pre');
        pre.textContent = text;

        wrapper.append(heading, pre);
        return wrapper;
    }

    function isValidYoutubeUrl(url) {
        // Basic YouTube URL validation
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
});
