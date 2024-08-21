api_url = "http://127.0.0.1:5000" 

function isValidUrl(element){
    if (element.length == 0){
        alert("Provide a valid URL!");
        return false;
    }
    return true;
} 

function getFileName(url, type){
  if (!url.includes("playlist")){
    if (type == "MP4"){
      return "video.mp4"
    }
    else {
      return "audio.mp3"
    }
  }
  return "playlist.zip"
}

function buttonActions(bool){
  mp4Button = document.getElementById("download-MP4-Button")
  mp3Button = document.getElementById("download-MP3-Button")
  mp4Button.disabled = !bool
  mp3Button.disabled = !bool
}

async function getContent(url, type){
    const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          type: type,
          url: url,
        }),
      };

      response = await fetch(
        `${api_url}/download-content`,
        options
      );

      return response;
}

async function downloadVideo(type){
    youtubeUrl = document.getElementById("youtube-url").value
    if (isValidUrl(youtubeUrl)) {
        waitMessage = document.getElementById("wait-message")
        waitMessage.textContent = "Please wait, downloading..."
        buttonActions(false)
        try {
          
          response = await getContent(youtubeUrl, type)

          if (!response.ok) {
            throw new Error("Failed to download content");
          }

          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = downloadUrl;
          a.download = getFileName(youtubeUrl, type)
          document.body.appendChild(a);
          const toastLiveExample = document.getElementById('liveToast')
          const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
          a.addEventListener('click', () => {
            toastBootstrap.show()
          })
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(downloadUrl);
        }
        catch(err) {
            alert(`Error: ${err}. Verify the URL and try again.`);
        }
        waitMessage.textContent = "";
        buttonActions(true)
    }
}