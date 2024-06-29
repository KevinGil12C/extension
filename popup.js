document.getElementById('downloadMP3').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      let url = tabs[0].url;
      console.log("Sending downloadMP3 message with URL:", url);
      chrome.tabs.sendMessage(tabs[0].id, {action: "downloadMP3", url: url}, (response) => {
        console.log("Response from content script:", response);
        alert(response.message);
      });
    });
  });
  
  document.getElementById('downloadMP4').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      let url = tabs[0].url;
      console.log("Sending downloadMP4 message with URL:", url);
      chrome.tabs.sendMessage(tabs[0].id, {action: "downloadMP4", url: url}, (response) => {
        console.log("Response from content script:", response);
        alert(response.message);
      });
    });
  });
  