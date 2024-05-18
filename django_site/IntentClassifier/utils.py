import requests
from openai import OpenAI
import json

FEW_SHOT_PROMPTS = """
    Record this rock that is blue and yellow 
    rock color
    Geo Sampling blue lithium rock, weighs around 40 pounds
    rock color, rock size
    Sample a basalt rock with a diameter of 10 inches
    rock type, rock size
    Here is a magenta, piece of granite. I found it in Arizona
    rock color, rock size, rock type, location
    Found basalt in Hadley Rille.
    rock type, location
    This is a red granite rock with a mass of 20 kg
    rock color, rock type, rock size
    This is Yash Patel, recording rock with mass of 400 grams and life in it
    astronaut name, rock size
    Identify this white limestone rock from the Grand Canyon from 1979
    rock color, rock type, location, year
    Sample a sedimentary rock with a length of 7 cm
    rock type, rock size
    Record a pink rock found by NASA astronauts on the lunar surface
    rock color, people, location
"""

class ExternalServiceClient:
    def __init__(self, base_url):
        self.base_url = base_url
        print("Initializating LLM Connection to: ", self.base_url)
        self.client = OpenAI(base_url=self.base_url, api_key="lm-studio")
        self.model = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"

    def execute_command(self, voice_command, prompt="Hello world"):
        print("Prompting LLM...")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": voice_command},
            ],
            temperature=0.7
        )
        resp = response.choices[0].message.content
                
        try:
            json_resp = json.loads(resp)
        except json.JSONDecodeError as e:
            print("Error parsing LLM-produced JSON")
            json_resp = {"error": "bad json parse", "response": resp}
        
        return json_resp