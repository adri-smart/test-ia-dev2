// KAN-487: Logic for the minimal conversational interface
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    let conversationId = null;
    let messageHistory = [];

    const addMessage = (sender, message, visualization = null) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        const textElement = document.createElement('p');
        textElement.innerText = message;
        messageElement.appendChild(textElement);

        // KAN-488: Handle visualizations
        if (visualization) {
            const vizContainer = document.createElement('div');
            vizContainer.classList.add('visualization-container');
            const canvas = document.createElement('canvas');
            vizContainer.appendChild(canvas);
            messageElement.appendChild(vizContainer);

            new Chart(canvas, {
                type: visualization.type,
                data: visualization.data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true
                }
            });
        }

        // KAN-489: Add feedback mechanism to assistant messages
        if (sender === 'assistant') {
            addFeedbackMechanism(messageElement);
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const handleSend = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        chatInput.value = '';
        chatInput.disabled = true;
        sendButton.disabled = true;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: conversationId,
                    messages: messageHistory
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            conversationId = data.conversation_id;
            messageHistory = data.messages;
            
            addMessage('assistant', data.text, data.visualization);

        } catch (error) {
            console.error('Error:', error);
            addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        } finally {
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.focus();
        }
    };

    sendButton.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });

    // Initial greeting
    addMessage('assistant', 'Hello! How can I help you with your customer data today?');
});

// KAN-489: Function to add feedback UI to a message
function addFeedbackMechanism(messageElement) {
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-container';
    
    const starsContainer = document.createElement('span');
    starsContainer.className = 'stars';
    starsContainer.innerHTML = 'Rate this insight: ';
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('span');
        star.className = 'star';
        star.innerHTML = '☆';
        star.dataset.rating = i;
        starsContainer.appendChild(star);
    }
    
    const commentContainer = document.createElement('div');
    commentContainer.className = 'feedback-comment';
    commentContainer.innerHTML = `
        <textarea placeholder="Optional: Add a comment..."></textarea>
        <button>Send Feedback</button>
    `;

    feedbackContainer.appendChild(starsContainer);
    feedbackContainer.appendChild(commentContainer);
    messageElement.appendChild(feedbackContainer);

    // Event listeners for feedback
    starsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('star')) {
            const rating = e.target.dataset.rating;
            // Show comment box after rating
            commentContainer.style.display = 'block';
            // Highlight selected stars
            Array.from(starsContainer.children).forEach(child => {
                if(child.classList.contains('star')) {
                    child.innerHTML = child.dataset.rating <= rating ? '★' : '☆';
                }
            });
            commentContainer.querySelector('button').dataset.rating = rating;
        }
    });

    commentContainer.querySelector('button').addEventListener('click', async (e) => {
        const rating = e.target.dataset.rating;
        const comment = commentContainer.querySelector('textarea').value;
        
        try {
            await fetch('http://127.0.0.1:5000/api/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rating, comment, insight_id: 'some_unique_id' })
            });
            feedbackContainer.innerHTML = '<em>Thank you for your feedback!</em>';
        } catch (error) {
            console.error('Feedback submission failed:', error);
            feedbackContainer.innerHTML = '<em>Could not submit feedback.</em>';
        }
    });
}
