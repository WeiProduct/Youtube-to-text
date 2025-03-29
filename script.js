document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('youtube-form');
    const resultContainer = document.getElementById('result-container');
    const statusMessage = document.getElementById('status-message');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    const API_URL = 'https://your-backend-service.com/api/convert';
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const youtubeUrl = document.getElementById('youtube-url').value.trim();
        
        if (!isValidYoutubeUrl(youtubeUrl)) {
            alert('Please enter a valid YouTube URL');
            return;
        }
        
        resultContainer.classList.remove('hidden');
        statusMessage.textContent = 'Processing your request. This may take a few minutes...';
        loadingSpinner.style.display = 'block';
        
        simulateBackendProcessing(youtubeUrl);
    });
    
    function isValidYoutubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
    
    function simulateBackendProcessing(url) {
        setTimeout(() => {
            statusMessage.innerHTML = `
                <p>✅ Processing complete!</p>
                <p><strong>Note:</strong> This is a simulation. In a real implementation, this would connect to a backend server running the Python code.</p>
                <p>The backend would need to use the provided Python code to:</p>
                <ol>
                    <li>Download the YouTube audio using yt-dlp</li>
                    <li>Convert the audio to text using a speech recognition service</li>
                    <li>Return the transcribed text</li>
                </ol>
                <div class="info-box">
                    <p><strong>Important:</strong> GitHub Pages can only host static content. To make this work, you would need:</p>
                    <ul>
                        <li>A separate server to run the Python code (e.g., Heroku, AWS, etc.)</li>
                        <li>An API endpoint on that server to accept YouTube URLs</li>
                        <li>CORS configuration to allow requests from your GitHub Pages site</li>
                    </ul>
                </div>
            `;
            loadingSpinner.style.display = 'none';
        }, 3000);
    }
}); 