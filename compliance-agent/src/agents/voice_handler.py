import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import time
import winsound
from pathlib import Path
from groq import Groq
import edge_tts
import asyncio

class VoiceHandler:
    def __init__(self):
        print("Initializing Voice Handler...")
        # Initialize Groq client
        self.groq = Groq(api_key= "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")
        self.conversation = []
        # Set up Edge TTS voice
        self.tts_voice = "en-US-ChristopherNeural"
        
        # Create temp directory
        self.temp_dir = Path("temp_audio")
        self.temp_dir.mkdir(exist_ok=True)
        
    def record_audio(self, duration=5, fs=16000):
        """Record audio from microphone"""
        try:
            print("Recording in 3 seconds...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            # Play beep sound
            winsound.Beep(1000, 500)
            
            print("Recording... (speak now)")
            
            # Record audio
            recording = sd.rec(
                int(duration * fs),
                samplerate=fs,
                channels=1,
                dtype=np.float32
            )
            sd.wait()
            print("Recording finished")
            
            # Ensure the temp directory exists
            self.temp_dir.mkdir(exist_ok=True)
            
            # Save audio with absolute path
            audio_path = (self.temp_dir / "recording.wav").resolve()
            sf.write(str(audio_path), recording, fs)
            
            # Verify file was created
            if audio_path.exists():
                print(f"Audio saved successfully at: {audio_path}")
                return str(audio_path)
            else:
                print("Failed to save audio file")
                return None
            
        except Exception as e:
            print(f"Error in recording: {str(e)}")
            return None
    
    def transcribe_audio(self, audio_path, fs=None):
        """Transcribe audio using Groq's Whisper API"""
        try:
            if not audio_path or not os.path.exists(audio_path):
                return "Error: No audio recorded"
            
            print(f"Transcribing audio from: {audio_path}")
            
            # Open the file in binary mode
            with open(audio_path, 'rb') as audio_file:
                # Create a tuple with filename and file content
                file_tuple = ('audio.wav', audio_file, 'audio/wav')
                
                # Call Groq's Whisper API with proper parameters
                transcription = self.groq.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=file_tuple,
                    language="en",
                    response_format="text",
                    temperature=0.0,
                    prompt="Transcribe the following audio from a customer service call."
                )
            
            # Get transcription text
            text = str(transcription)
            text = text.strip()
            
            if not text:
                text = "No speech detected"
            
            print(f"Transcription completed: {text}")
            
            # Cleanup
            try:
                Path(audio_path).unlink(missing_ok=True)
                print("Audio file cleaned up")
            except Exception as e:
                print(f"Cleanup error: {str(e)}")
            
            return text
            
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            if os.path.exists(audio_path):
                print(f"Audio file exists at: {audio_path}")
                print(f"File size: {os.path.getsize(audio_path)} bytes")
                
                # Try to read the audio file to verify its contents
                try:
                    with open(audio_path, 'rb') as f:
                        content = f.read()
                        print(f"Audio file is readable, size: {len(content)} bytes")
                except Exception as read_error:
                    print(f"Error reading audio file: {str(read_error)}")
            
            return "Error in transcription"
    
    async def _async_tts(self, text, output_file):
        """Async function to generate speech using Edge TTS"""
        communicate = edge_tts.Communicate(text, self.tts_voice)
        await communicate.save(output_file)
    
    def text_to_speech(self, text):
        """Convert text to speech using Edge TTS"""
        try:
            # Create output path with absolute path
            output_path = (self.temp_dir / "speech.mp3").resolve()
            
            # Generate speech
            asyncio.run(self._async_tts(text, str(output_path)))
            
            # Play the audio
            data, fs = sf.read(str(output_path))
            sd.play(data, fs)
            sd.wait()
            
            # Cleanup
            try:
                output_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Cleanup error: {str(e)}")
            
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            print(f"Text that should have been spoken: {text}")
            time.sleep(2)
    
    def add_to_conversation(self, speaker: str, text: str):
        """Add utterance to conversation"""
        self.conversation.append(f"{speaker}: {text}")
    
    def get_transcript(self):
        """Get complete conversation transcript"""
        return "\n".join(self.conversation)
    
    def save_transcript(self, filename):
        """Save conversation transcript to file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.get_transcript())
    
    def __del__(self):
        """Cleanup temp directory on exit"""
        try:
            import shutil
            shutil.rmtree(str(self.temp_dir), ignore_errors=True)
        except:
            pass 