console.log("Content script loaded.");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received in content script:", message);
  if (message.action === "downloadMP3" || message.action === "downloadMP4") {
    console.log(`Starting download for ${message.action} with URL: ${message.url}`);
    fetch(`http://localhost:8000/${message.action}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: message.url })
    })
    .then(response => {
      console.log("Fetch response received:", response);
      return response.json();
    })
    .then(data => {
      console.log("JSON response from server:", data);
      sendResponse(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  return true;  // Keeps the message channel open for sendResponse
});
