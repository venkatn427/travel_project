const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Function to add a message to the chat output
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatOutput.appendChild(messageElement);
}

// Event listener for the send button
sendButton.addEventListener('click', function() {
    const userMessage = userInput.value;
    addMessage(userMessage, "You");
    // You can add logic here to handle the user's message and generate a chatbot response.
    // For now, let's assume a simple response.
    const chatbotResponse = 'This is a chatbot response.';
    addMessage(chatbotResponse, 'Chatbot');
    userInput.value = ''; // Clear the input field
});

// You can also handle pressing Enter to send a message
userInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});