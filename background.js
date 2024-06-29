chrome.action.onClicked.addListener((tab) => {
  console.log("Extension icon clicked, executing content script...");
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js']
  });
});
