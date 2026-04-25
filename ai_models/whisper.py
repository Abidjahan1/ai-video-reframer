"""
WhisperModel: Wrapper for OpenAI Whisper speech-to-text model.

Key Concepts:
- Whisper: OpenAI's automatic speech recognition (ASR) model.
- OOP: Encapsulates speech-to-text logic for modularity.
"""

from utils.performance_mode import get_performance_mode

class WhisperModel:
    def __init__(self, config):
        """
        Initialize the Whisper model.
        Args:
            config (AppConfig): Application configuration.
        """
        self.config = config
        self.performance_mode = get_performance_mode()
        # Load Whisper model with correct backend
        if self.performance_mode == 'gpu':
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        # Future: Load model weights with self.device

    def transcribe(self, audio_path):
        """
        Placeholder for transcription method.
        Args:
            audio_path (str): Path to the audio file.
        Returns:
            str: Transcribed text (to be implemented).
        """
        # Use self.device for inference
        return ""
