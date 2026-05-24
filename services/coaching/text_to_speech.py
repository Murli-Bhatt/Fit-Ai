import io
import base64
from gtts import gTTS

def text_to_speech_base64(text: str) -> str:
    """
    Converts text to speech using gTTS and returns its Base64 representation.
    Runs entirely in memory using BytesIO, avoiding temporary file overhead.
    Returns:
        str: Base64 encoded string of MP3 audio, or empty string on failure.
    """
    if not text or not text.strip():
        return ""
        
    try:
        # Convert text to audio in memory
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Read bytes and encode to base64
        audio_bytes = fp.read()
        b64 = base64.b64encode(audio_bytes).decode('utf-8')
        return b64
        
    except Exception as e:
        print(f"gTTS conversion failed: {str(e)}")
        return ""
