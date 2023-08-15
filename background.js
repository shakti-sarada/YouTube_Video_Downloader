chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  const port = chrome.runtime.connectNative("your.native.messaging.host");
  port.postMessage({ url: message.url });

  port.onMessage.addListener((response) => {
    console.log("Received response:", response);
    sendResponse(response);
  });

  port.onDisconnect.addListener(() => {
    if (chrome.runtime.lastError) {
      console.error("Error Connecting:", chrome.runtime.lastError);
    }
  });
  return true;
});
