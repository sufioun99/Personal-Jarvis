"""
Voice Interface - Speech-to-Text and Text-to-Speech
"""
import asyncio
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import io
from config import settings
from utils.logger import logger

try:
    from elevenlabs import generate, play as elevenlabs_play, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logger.warning("ElevenLabs not available, falling back to gTTS")


class VoiceInterface:
    """
    Handles speech-to-text and text-to-speech operations
    """
    
    def __init__(self):
        """Initialize voice interface"""
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.wake_word = settings.wake_word.lower()
        
        # Initialize ElevenLabs if available
        if ELEVENLABS_AVAILABLE and settings.elevenlabs_api_key:
            set_api_key(settings.elevenlabs_api_key)
            self.use_elevenlabs = True
            logger.info("ElevenLabs TTS enabled")
        else:
            self.use_elevenlabs = False
            logger.info("Using gTTS for text-to-speech")
    
    def initialize_microphone(self):
        """Initialize microphone for speech recognition"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            self.microphone = None
    
    async def listen_for_wake_word(self) -> bool:
        """
        Listen for wake word activation
        
        Returns:
            True if wake word detected, False otherwise
        """
        if not self.microphone:
            self.initialize_microphone()
        
        if not self.microphone:
            logger.error("No microphone available")
            return False
        
        try:
            with self.microphone as source:
                logger.info(f"Listening for wake word: '{self.wake_word}'")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            logger.debug(f"Heard: {text}")
            
            if self.wake_word in text:
                logger.info("Wake word detected!")
                return True
            return False
            
        except sr.WaitTimeoutError:
            return False
        except Exception as e:
            logger.error(f"Error in wake word detection: {e}")
            return False
    
    async def speech_to_text(self, timeout: int = 10) -> Optional[str]:
        """
        Convert speech to text
        
        Args:
            timeout: Maximum time to listen
            
        Returns:
            Transcribed text or None
        """
        if not self.microphone:
            self.initialize_microphone()
        
        if not self.microphone:
            logger.error("No microphone available")
            return None
        
        try:
            with self.microphone as source:
                logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            # Try multiple recognition services
            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Recognition service error: {e}")
                # Try alternative service
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    logger.info(f"Recognized (Sphinx): {text}")
                    return text
                except:
                    return None
                    
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    async def text_to_speech(self, text: str, voice: str = "default") -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            voice: Voice ID (for ElevenLabs)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_elevenlabs:
                # Use ElevenLabs for high-quality voice
                audio = generate(text=text, voice=voice if voice != "default" else "Adam")
                elevenlabs_play(audio)
            else:
                # Use gTTS as fallback
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save to temporary file and play
                with io.BytesIO() as fp:
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    audio = AudioSegment.from_mp3(fp)
                    play(audio)
            
            logger.info("Speech output completed")
            return True
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return False
    
    async def listen_and_transcribe(self) -> Optional[str]:
        """
        Wait for wake word, then transcribe command
        
        Returns:
            Transcribed command or None
        """
        # Wait for wake word
        if await self.listen_for_wake_word():
            await self.text_to_speech("Yes, how can I help?")
            # Listen for actual command
            return await self.speech_to_text()
        return None


# Global voice interface instance
voice_interface = VoiceInterface()
