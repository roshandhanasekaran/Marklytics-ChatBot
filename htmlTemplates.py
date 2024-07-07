# htmlTemplates.py

css = '''
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #333;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: #fff;
}
.chat-container {
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
    padding: 1rem;
    background-color: #072AF5;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    height: 80vh;
    color: #333;
}
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    background-color: #072AF5;
}
.chat-message {
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    display: flex;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.chat-message.user {
    background-color: #e6e1ff;
    align-self: flex-end;
}
.chat-message.bot {
    background-color: #dcdcdc;
    align-self: flex-start;
}
.chat-message .avatar {
    width: 15%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
}
.chat-input {
    display: flex;
    padding: 0.5rem;
    border-top: 1px solid #ddd;
}
.chat-input input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 0.5rem;
    font-size: 1rem;
}
.chat-input button {
    padding: 0.75rem 1.5rem;
    border: none;
    background-color: #072AF5;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}
.chat-input button:hover {
    background-color: #5753c9;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.imgur.com/tTK3N0v.jpg" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://res.cloudinary.com/dc3t0ei2e/image/upload/v1713509894/fwk0kvbrh26oukttk3jh.jpg" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

html = f'''
{css}
<div class="chat-container">
    <div class="chat-messages" id="chat-messages">
        {user_template.replace('{{MSG}}', 'Hello! How can I assist you today?')}
        {bot_template.replace('{{MSG}}', 'Hi there! How can I help you?')}
    </div>
    <div class="chat-input">
        <input type="text" id="user-input" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
<script>
function sendMessage() {{
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message === '') return;

    const chatMessages = document.getElementById('chat-messages');

    // User message
    const userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    userMessage.innerHTML = `
        <div class="avatar">
            <img src="https://res.cloudinary.com/dc3t0ei2e/image/upload/v1713509894/fwk0kvbrh26oukttk3jh.jpg" alt="User Avatar">
        </div>
        <div class="message">$${{message}}</div>
    `;
    chatMessages.appendChild(userMessage);

    // Bot response
    const botMessage = document.createElement('div');
    botMessage.className = 'chat-message bot';
    botMessage.innerHTML = `
        <div class="avatar">
            <img src="https://res.cloudinary.com/dc3t0ei2e/image/upload/v1713509894/o09w7mwri7ugvqr4luk1.jpg" alt="Bot Avatar">
        </div>
        <div class="message">This is a default response.</div>
    `;
    chatMessages.appendChild(botMessage);

    // Clear input
    userInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}}
</script>
'''

# Save the generated HTML content to index.html
with open('index.html', 'w') as file:
    file.write(html)
