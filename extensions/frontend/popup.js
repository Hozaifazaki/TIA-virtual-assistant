document.addEventListener('DOMContentLoaded', () => {
  const sendBtn = document.getElementById('sendBtn');
  const userInput = document.getElementById('userInput');
  const chatHistory = document.getElementById('chatHistory');

  if (sendBtn && userInput && chatHistory) {
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  } else {
    console.error('Required elements not found');
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
      addMessageToChat('user', message);
      userInput.value = '';

      chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {action: "getPageContent"}, (pageContent) => {
          if (chrome.runtime.lastError) {
            console.error('Error getting page content:', chrome.runtime.lastError);
            addMessageToChat('ai', 'Failed to get page content. Please refresh the page and try again.');
            return;
          }

          fetch('http://localhost:8000/ai-assistant', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_prompt: message,
              webpage_content: pageContent
            })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            addMessageToChat('ai', data.assistant_response);
          })
          .catch(error => {
            console.error('Error:', error);
            addMessageToChat('ai', `An error occurred: ${error.message}. Please try again.`);
          });
        });
      });
    }
  }

  function addMessageToChat(sender, text) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);

    if (sender === 'ai') {
      messageElement.innerHTML = marked.parse(text);
    } else {
      messageElement.textContent = text;
    }

    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }
});
