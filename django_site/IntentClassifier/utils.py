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
        self.openai_client = OpenAI(api_key="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")

    def make_request(self, endpoint, data=None):
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )
        return response.choices[0].message

        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     # You might want to handle errors more gracefully
        #     raise Exception(f"Request failed with status code {response.status_code}")

    def execute_command(self, voice_command, tags):
        tags_str = ", ".join(tags)
        prompt = f"""
            Can you take this sentence: {voice_command} and extract the tags of {tags_str} and if its not there put null.
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":"""
                    You are a helpful assistant.
                    You will give the result of my query in the following format:
                    {"tag1":"value of tag1", "tag2":"value of tag2"}
                """},
                {"role": "user", "content": prompt},
            ]
        )
        resp = response.choices[0].message.content
        json_resp = json.loads(resp)

        return json_resp