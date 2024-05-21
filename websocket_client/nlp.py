
import copy
import requests
import json

def transcription_endpoint(body, SERVER_URL):
    """
    BODY IS A JSON OBJ
    """

    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    resp = requests.post(f"{SERVER_URL}/IntentClassifier/transcription/", headers=headers, data=json.dumps(body))
    
    print(resp.json())
    transcription_text = resp.json()['text_from_VEGA']
    print("Transcribed: ", transcription_text)
    

    # # Create the payload
    # json_resp = {
    #     "id": "Astronaut_001",
    #     "type": "AUDIO",
    #     "use": "PUT",
    #     "data": {
    #         "base_64_audio": "",
    #         "text_from_VEGA": transcription_text,
    #         "command": []
    #     }
    # }

    json_resp = copy.deepcopy(body)
    
    json_resp['data']['base_64_audio'] = "" # clear audio file so its not gimungus
    json_resp['data']['text_from_VEGA'] = transcription_text
    json_resp['type'] = "AUDIO_PROCESSED"
    print(json_resp)

    # resp_class = requests.post(f"{SERVER_URL}/IntentClassifier/webhook/", headers=headers, data=json.dumps(json_resp))
    # print(resp_class.json())
    # json_resp['data']['command'] = resp_class.json()['command']
    # print(json_resp)

    return json_resp