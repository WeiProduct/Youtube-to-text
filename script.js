document.addEventListener('DOMContentLoaded', function() {
    const backendUrl = "https://youtube-to-text-backend-77ca40ac4b99.herokuapp.com";
    const convertBtn = document.getElementById('convertBtn');
    const youtubeUrlInput = document.getElementById('youtubeUrl');
    const statusElement = document.getElementById('status');
    
    convertBtn.addEventListener('click', async function() {
        const youtubeUrl = youtubeUrlInput.value.trim();
        
        if (!youtubeUrl) {
            statusElement.innerHTML = `
                <h2 class="error">❌ Error</h2>
                <div class="error-details">Please enter a YouTube URL</div>
            `;
            return;
        }
        
        // Show loading status
        statusElement.innerHTML = `
            <h2>Processing...</h2>
            <p>Downloading audio from YouTube and converting to text. This may take a minute.</p>
        `;
        
        try {
            const response = await fetch(`${backendUrl}/api/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ youtube_url: youtubeUrl })
            });
            
            const data = await response.json();
            handleApiResponse(data);
        } catch (error) {
            statusElement.innerHTML = `
                <h2 class="error">❌ Error</h2>
                <div class="error-details">Failed to connect to the server. Please try again later.</div>
                <div class="limitations-box">
                    <p>The backend server might be in sleep mode. Please try again in a few seconds.</p>
                </div>
            `;
        }
    });
});

function handleApiResponse(data) {
    const statusElement = document.getElementById('status');
    
    if (data.success) {
        // Successfully converted
        statusElement.innerHTML = `
            <h2 class="success">✅ Conversion Complete!</h2>
            <div class="result-container">
                <h3>Transcription Result:</h3>
                <div class="transcription-text">${data.text}</div>
                <button class="download-btn" onclick="downloadText('${encodeURIComponent(data.text)}')">Download Text</button>
            </div>
        `;
    } else {
        // Error occurred
        let errorMessage = data.error || "An unknown error occurred";
        let helpMessage = "";
        
        // Check if this is a YouTube restriction error
        if (errorMessage.includes("Sign in to confirm you're not a bot") || 
            errorMessage.includes("HTTP Error 400") ||
            errorMessage.includes("HTTP Error 429") ||
            errorMessage.includes("All download methods failed")) {
            
            helpMessage = `
                <div class="limitations-box">
                    <h3>Why this happens:</h3>
                    <p>YouTube actively blocks automated downloads from cloud servers like Heroku. This is because:</p>
                    <ul>
                        <li>YouTube detects our server as a bot and requires human verification</li>
                        <li>Cloud server IP addresses (like Heroku's) are often blocked</li>
                        <li>No browser cookies are available on the server</li>
                    </ul>
                    
                    <h3>Alternatives you can try:</h3>
                    <ul>
                        <li>Use a browser extension for YouTube transcription</li>
                        <li>Try a desktop application that runs locally on your computer</li>
                        <li>Use YouTube's built-in auto-generated captions when available</li>
                        <li>Use a paid transcription service that has proper YouTube API access</li>
                    </ul>
                </div>
            `;
        }
        
        statusElement.innerHTML = `
            <h2 class="error">❌ Error</h2>
            <div class="error-details">${errorMessage}</div>
            ${helpMessage}
        `;
    }
}

function downloadText(text) {
    const decodedText = decodeURIComponent(text);
    const blob = new Blob([decodedText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transcription.txt';
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
} 