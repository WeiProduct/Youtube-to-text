document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('youtube-form');
    const resultContainer = document.getElementById('result-container');
    const statusMessage = document.getElementById('status-message');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    // Backend API URL - This would point to your actual backend service
    // For demonstration purposes, we'll use a placeholder
    const API_URL = 'https://your-backend-service.com/api/convert';
    
    form.addEventListener('submit', function(e) {
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
        
        // In a real implementation, you would send the URL to your backend
        // For demonstration, we'll simulate a response after 3 seconds
        simulateBackendProcessing(youtubeUrl);
    });
    
    function isValidYoutubeUrl(url) {
        // Basic YouTube URL validation
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
    
    function simulateBackendProcessing(url) {
        // This function simulates what would happen with a real backend
        // In a real implementation, you would make an API call to your server
        
        setTimeout(() => {
            // Simulate success response
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