document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('user-input');
    const outputArea = document.getElementById('chat-output');

    inputField.addEventListener('keypress', async function(e) {
        if (e.key === 'Enter' && this.value.trim() !== '') {
            const userMessage = this.value.trim();
            
            // Add user message to chat
            appendMessage('user', userMessage);
            
            // Clear input field
            this.value = '';
            
            try {
                // Send message to backend
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: userMessage })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Add bot response to chat
                appendMessage('bot', data.response);
                
            } catch (error) {
                appendMessage('bot', 'Entschuldigung, es ist ein Fehler aufgetreten: ' + error.message);
            }
        }
    });

    function appendMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        messageDiv.textContent = content;
        outputArea.appendChild(messageDiv);
        outputArea.scrollTop = outputArea.scrollHeight;
    }
});
