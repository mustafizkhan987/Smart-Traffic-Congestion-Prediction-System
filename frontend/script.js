document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Set loading state
    const btn = document.querySelector('.btn');
    const originalText = btn.textContent;
    btn.textContent = 'Analyzing Model...';
    btn.disabled = true;
    
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        const level = data.prediction;
        
        // Update UI
        const resultBox = document.getElementById('result');
        const levelIndicator = document.getElementById('congestion-level');
        
        levelIndicator.textContent = level;
        
        // Reset classes
        levelIndicator.className = 'level-indicator';
        if (level === 'Low') {
            levelIndicator.classList.add('level-low');
        } else if (level === 'Medium') {
            levelIndicator.classList.add('level-medium');
        } else if (level === 'High') {
            levelIndicator.classList.add('level-high');
        }
        
        // Show result box
        resultBox.classList.remove('hidden');
        
    } catch (error) {
        console.error('Error fetching prediction:', error);
        alert('Failed to get prediction from the backend API. Ensure the FastAPI server is running at http://127.0.0.1:8000.');
    } finally {
        // Restore button state
        btn.textContent = originalText;
        btn.disabled = false;
    }
});
