"""
Multi-language Speech Recognition using OpenAI Whisper
"""
import logging
import tempfile
import os
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    Multi-language speech recognition system
    """
    
    def __init__(self):
        self._init_whisper()
    
    def _init_whisper(self):
        """Initialize Whisper client"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=api_key)
                logger.info("Whisper speech recognition initialized")
            else:
                self.client = None
                logger.warning("OpenAI API key not found for speech recognition")
        except Exception as e:
            logger.error(f"Error initializing Whisper: {str(e)}")
            self.client = None
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: str = "en"
    ) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio file data
            language: Language code (e.g., 'en', 'es', 'fr', 'de', 'ja', 'zh')
        
        Returns:
            Transcribed text
        """
        if not self.client:
            return "Speech recognition not configured (OpenAI API key required)"
        
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            try:
                # Transcribe using Whisper
                with open(temp_audio_path, "rb") as audio_file:
                    transcript = await self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language if language != "auto" else None
                    )
                
                return transcript.text
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)
                    
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return f"Error transcribing audio: {str(e)}"
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "nl", "name": "Dutch"},
            {"code": "ru", "name": "Russian"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "ar", "name": "Arabic"},
            {"code": "hi", "name": "Hindi"},
            {"code": "auto", "name": "Auto-detect"}
        ]
