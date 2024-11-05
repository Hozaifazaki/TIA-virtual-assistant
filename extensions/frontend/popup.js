// Global variables
let userMessage = "";

document.addEventListener('DOMContentLoaded', () => {
  const sendButton = document.getElementById('sendBtn');
  const clearButton = document.getElementById('clearBtn');
  const inputTextArea = document.getElementById('userInput');
  const chatArea = document.getElementById('chatHistory');

  if (sendButton && clearButton && inputTextArea && chatArea) {
    sendButton.addEventListener('click', sendMessage);
    clearButton.addEventListener('click', clearMessages);
    inputTextArea.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  } else {
    console.error('Required elements not found');
  }

  function sendMessage() {
    const newMessage = inputTextArea.value.trim();

    if (newMessage && userMessage === "") {
      userMessage = newMessage;
      addMessageToChat('user', userMessage);
      inputTextArea.value = '';

      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "getPageContent" }, (pageContent) => {
          if (chrome.runtime.lastError) {
            console.error('Error getting page content:', chrome.runtime.lastError);
            addMessageToChat('ai', 'Failed to get page content. Continue without scraping');
          }

          if (!pageContent) {
            console.log('No webpage content found. Sending empty string to API.');
            pageContent = ''; // Set to empty string
          }

          const aiMessageBubble = addMessageToChat('ai', '...');
          let accumulatedResponse = '';

          fetch('http://localhost:8000/ai-assistant', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_prompt: userMessage,
              webpage_content: pageContent
            })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function readStream() {
              return reader.read().then(({ done, value }) => {
                if (done) {
                  return;
                }
                const chunk = decoder.decode(value, { stream: true });
                accumulatedResponse += chunk;
                aiMessageBubble.innerHTML = marked.parse(accumulatedResponse);
                chatArea.scrollTop = chatArea.scrollHeight;
                return readStream();
              });
            }

            return readStream();
          })
          .then(() => {
            userMessage = ""; // Reset after successful completion
          })
          .catch(error => {
            console.error('Error:', error);
            addMessageToChat('ai', `An error occurred: ${error.message}. Please try again.`);
            userMessage = ""; // Reset even if there's an error
          });
        });
      });
    }
  }

  function addMessageToChat(sender, text) {
    const messageBubble = document.createElement('div');
    messageBubble.classList.add('message', `${sender}-message`);

    if (sender === 'ai') {
      messageBubble.innerHTML = marked.parse(text);
    } else {
      messageBubble.textContent = text;
    }

    chatArea.appendChild(messageBubble);
    chatArea.scrollTop = chatArea.scrollHeight;
    return messageBubble;
  }

  function clearMessages() {
    chatArea.innerHTML = '';
  }
});
