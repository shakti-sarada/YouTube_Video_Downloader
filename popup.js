document.getElementById("downloadButton").addEventListener("click", () => {
  chrome.scripting.executeScript({
    target: { tabId: tabId },
    function: downloadYouTubeVideo,
  });
});

function downloadYouTubeVideo() {
  const videoUrl = window.location.href;
  chrome.runtime.sendMessage({ url: videoUrl });
}
