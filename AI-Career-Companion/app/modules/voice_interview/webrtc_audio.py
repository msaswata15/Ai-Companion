# app/modules/voice_interview/webrtc_audio.py
"""
WebRTC Audio Recording Module for Streamlit Interview App
Handles live audio recording, processing, and conversion
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np
import wave
import os
import uuid
import threading
from typing import List
import logging

# Set up logging
logger = logging.getLogger(__name__)

def initialize_webrtc_session_state():
    """Initialize session state variables for WebRTC audio recording"""
    if 'audio_frames' not in st.session_state:
        st.session_state.audio_frames = []
    if 'recording_complete' not in st.session_state:
        st.session_state.recording_complete = False
    if 'audio_file_path' not in st.session_state:
        st.session_state.audio_file_path = None
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False

class AudioProcessor:
    """Thread-safe audio frame processor for WebRTC streams"""
    
    def __init__(self):
        self.audio_frames: List[av.AudioFrame] = []
        self.lock = threading.Lock()
    
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        """Receive and store audio frames from WebRTC stream"""
        with self.lock:
            self.audio_frames.append(frame)
        return frame
    
    def get_audio_frames(self):
        """Get a copy of all stored audio frames"""
        with self.lock:
            return self.audio_frames.copy()
    
    def clear_frames(self):
        """Clear all stored audio frames"""
        with self.lock:
            self.audio_frames.clear()

def save_audio_frames_to_wav(audio_frames: List[av.AudioFrame], output_path: str) -> str:
    """
    Convert PyAV audio frames to WAV file optimized for Assembly AI
    
    Args:
        audio_frames: List of PyAV audio frames
        output_path: Path where to save the WAV file
        
    Returns:
        str: Path to the saved WAV file
    """
    if not audio_frames:
        raise ValueError("No audio frames to save")
    
    # Get audio properties from first frame
    sample_rate = audio_frames[0].sample_rate
    channels = len(audio_frames[0].layout.channels)
    
    logger.info(f"Processing {len(audio_frames)} frames - Sample rate: {sample_rate}, Channels: {channels}")
    
    # Collect all audio data
    audio_data = []
    for frame in audio_frames:
        # Convert frame to numpy array
        array = frame.to_ndarray()
        
        # Convert to 16-bit integer if needed
        if array.dtype != np.int16:
            if array.dtype == np.float32:
                array = (array * 32767).astype(np.int16)
            elif array.dtype == np.float64:
                array = (array * 32767).astype(np.int16)
        
        audio_data.append(array)
    
    if not audio_data:
        raise ValueError("No audio data extracted from frames")
    
    # Concatenate all audio data
    full_audio = np.concatenate(audio_data, axis=0)
    
    # Ensure mono (mix channels if stereo)
    if len(full_audio.shape) > 1 and full_audio.shape[1] > 1:
        full_audio = np.mean(full_audio, axis=1).astype(np.int16)
    
    # Write WAV file optimized for speech recognition
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)        # Mono
        wav_file.setsampwidth(2)        # 16-bit
        wav_file.setframerate(16000)    # 16kHz for speech recognition
        
        # Resample if necessary (simple linear interpolation)
        if sample_rate != 16000:
            target_length = int(len(full_audio) * 16000 / sample_rate)
            indices = np.linspace(0, len(full_audio) - 1, target_length)
            full_audio = np.interp(indices, np.arange(len(full_audio)), full_audio).astype(np.int16)
        
        wav_file.writeframes(full_audio.tobytes())
    
    duration = len(full_audio) / 16000
    logger.info(f"Saved audio to {output_path} - Duration: {duration:.2f}s")
    return output_path

def create_webrtc_recorder():
    """
    Create and return a WebRTC audio recorder component
    
    Returns:
        WebRTC context object
    """
    # Initialize session state
    initialize_webrtc_session_state()
    
    # Create audio processor if not exists
    if 'audio_processor' not in st.session_state:
        st.session_state.audio_processor = AudioProcessor()
    
    # WebRTC configuration
    rtc_configuration = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
    
    # Create WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="audio-recorder",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={
            "audio": {
                "sampleRate": 16000,
                "channelCount": 1,
                "echoCancellation": True,
                "noiseSuppression": True,
                "autoGainControl": True,
            },
            "video": False,
        },
        audio_frame_callback=st.session_state.audio_processor.recv,
        async_processing=True,
    )
    
    return webrtc_ctx

def process_recorded_audio():
    """
    Process recorded audio frames and save to WAV file
    
    Returns:
        str: Path to saved audio file or None if failed
    """
    try:
        # Get recorded frames
        audio_frames = st.session_state.audio_processor.get_audio_frames()
        
        if not audio_frames:
            st.error("❌ No audio data recorded. Please try again.")
            return None
        
        # Create output directory
        output_dir = "temp_audio"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"interview_audio_{uuid.uuid4().hex[:8]}.wav"
        audio_path = os.path.join(output_dir, filename)
        
        # Save audio to WAV file
        save_audio_frames_to_wav(audio_frames, audio_path)
        
        # Update session state
        st.session_state.audio_file_path = audio_path
        st.session_state.recording_complete = True
        
        logger.info(f"Successfully processed {len(audio_frames)} audio frames")
        return audio_path
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        st.error(f"❌ Error processing audio: {str(e)}")
        return None