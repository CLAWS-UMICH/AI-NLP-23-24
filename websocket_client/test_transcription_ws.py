import base64
import requests
import json
from nlp import transcription_endpoint

def encode_audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
    return base64_audio

def test_audio_transcription(endpoint_url, audio_file_path):
    # Encode the audio file to base64
    base64_audio = encode_audio_to_base64(audio_file_path)
    
    # Create the payload
    payload = {
        "id": "Astronaut_001",
        "type": "AUDIO",
        "use": "PUT",
        "data": {
            "base_64_audio": base64_audio,
            "text_from_VEGA": "",
            "command": []
        }
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    resp = transcription_endpoint(payload, "http://localhost:8000")
    print(resp)

if __name__ == "__main__":
    # Replace with the actual endpoint URL
    endpoint_url = "http://localhost:8000/IntentClassifier/transcription/"
    
    # Replace with the path to your test MP3 file
    audio_file_path = "../django_site/test2.mp3"
    
    test_audio_transcription(endpoint_url, audio_file_path)

