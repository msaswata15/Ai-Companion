import streamlit.components.v1 as components
import json


def speech_recognizer():
    """
    Embeds a WebKit Speech Recognition component and returns the transcribed text.
    """
    html_code = r"""
    <div>
      <button id="start-btn">Start Recording</button>
      <button id="stop-btn" disabled>Stop Recording</button>
      <p id="status">Click Start to begin recognition.</p>
      <textarea id="transcript" rows="5" cols="60"></textarea>
    </div>
    <script>
      const startBtn = document.getElementById('start-btn');
      const stopBtn = document.getElementById('stop-btn');
      const statusElem = document.getElementById('status');
      const transcriptElem = document.getElementById('transcript');
      
      let recognition;
      if (!('webkitSpeechRecognition' in window)) {
        statusElem.innerText = 'Speech Recognition not supported in this browser.';
      } else {
        recognition = new webkitSpeechRecognition();
        recognition.interimResults = true;
        recognition.continuous = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
          statusElem.innerText = 'Listening...';
          stopBtn.disabled = false;
          startBtn.disabled = true;
        };
        recognition.onend = () => {
          statusElem.innerText = 'Stopped.';
          stopBtn.disabled = true;
          startBtn.disabled = false;
          // send transcript to Streamlit
          window.parent.postMessage({transcript: transcriptElem.value}, '*');
        };
        recognition.onresult = (event) => {
          let interim = '';
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              transcriptElem.value += event.results[i][0].transcript + '\n';
            } else {
              interim += event.results[i][0].transcript;
            }
          }
        };

        startBtn.onclick = () => recognition.start();
        stopBtn.onclick = () => recognition.stop();
      }
    </script>
    """
    # Render and capture transcript via postMessage
    transcript = components.html(html_code, height=300)
    return transcript
