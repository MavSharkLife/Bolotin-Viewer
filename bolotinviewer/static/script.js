// Declares varibles
const videoStream = document.createElement('video')
videoStream.autoplay = true
videoStream.playsInline = true
let currentFacing = 'environment' // Defaults to back camera
let currentLabel = 'Nothing Detected'
const yoloCard = document.getElementById('yolo-card')
const micBtn = document.getElementById('mic-btn')

// Cancels text-to-speech queue
window.speechSynthesis.cancel()

// Text-to-speech process
micBtn.addEventListener('click', () => {
  window.speechSynthesis.cancel()
  const speak = new SpeechSynthesisUtterance(currentLabel)
  speak.volume = 1
  speak.rate = 1
  speak.pitch = 1
  window.speechSynthesis.speak(speak)
})

// Starts camera
function startCamera() {
  if (videoStream.srcObject) {
    videoStream.srcObject.getTracks().forEach((track) => track.stop())
  }
  const constraints = {
    video: {
      facingMode: currentFacing,
    },
  }
  // Request access to webcam
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      videoStream.srcObject = stream
    })
    // Catching errors
    .catch((error) => {
      console.error('Error accessing webcam:', error)

      if (currentFacing === 'environment') {
        console.log('Cannot access back camera, falling back.')
        navigator.mediaDevices
          .getUserMedia({ video: true })
          .then((s) => (videoStream.srcObject = s))
      }
    })
}

// Starting camera
startCamera()

// Camera rotate button functionality
const rotateBtn = document.getElementById('rotate-btn')
rotateBtn.addEventListener('click', () => {
  currentFacing = currentFacing === 'user' ? 'environment' : 'user'
  startCamera()
})

// Holds video frames in a canvas to convert to JPEG
const canvas = document.createElement('canvas')
const context = canvas.getContext('2d')
let isProcessing = false

// Sends the frame to YOLO
function processNextFrame() {
  // Checks if the image is ready and then sends it to the flask backend to be processed by the YOLO CNN
  if (
    videoStream.readyState === videoStream.HAVE_ENOUGH_DATA &&
    !isProcessing
  ) {
    isProcessing = true
    canvas.width = videoStream.videoWidth
    canvas.height = videoStream.videoHeight
    context.drawImage(videoStream, 0, 0, canvas.width, canvas.height)
    const imageData = canvas.toDataURL('image/jpeg', 0.5) // 0.5 is the quality of the image

    // Sends to server
    fetch('/video', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        frame: imageData,
      }),
    })
      .then((response) => response.json())

      // Sets the processed frame to an html element
      .then((data) => {
        if (data.frame) {
          const yoloCard = document.getElementById('yolo-card')
          yoloCard.src = data.frame
        }
        if (data.label) {
          currentLabel = data.label
          autoSpeak(currentLabel)
        }
      })
      // Resets processing and then requests the next frame
      .finally(() => {
        isProcessing = false
        requestAnimationFrame(processNextFrame)
      })
  } else {
    requestAnimationFrame(processNextFrame)
  }
}

// Calls to process the frame
videoStream.addEventListener('play', () => {
  processNextFrame()
})
