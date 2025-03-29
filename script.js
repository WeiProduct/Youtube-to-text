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
                statusMessage.innerHTML = `
                    <p>✅ Transcription complete!</p>
                    <div class="transcription-result">
                        <h3>Transcribed Text:</h3>
                        <pre>${data.text}</pre>
                    </div>
                `;
            } else {
                statusMessage.innerHTML = `
                    <p>❌ Error: ${data.error}</p>
                `;
            }
        } catch (error) {
            statusMessage.innerHTML = `
                <p>❌ Error: Could not connect to the server. Please try again later.</p>
                <p>Details: ${error.message}</p>
            `;
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });
    
    function isValidYoutubeUrl(url) {
        // Basic YouTube URL validation
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
}); 