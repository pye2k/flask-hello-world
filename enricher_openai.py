from openai import OpenAI
from catalog_enricher import CatalogEnricher
import json, re

class OpenAIEnricher(CatalogEnricher):

    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def enrich_from_image(self, image_url, additional_context):
        client = OpenAI()

        # Retrieve the handle to the "Catalog descriptions from images" Assistant
        assistant = client.beta.assistants.retrieve("asst_tL7qx1mIDxeZQuwvdH1BNM5n")
        self.model = assistant.model

        # Create a thread (a conversation between user and agent)
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": additional_context
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
        )

        # Create a run, and poll for completion
        run = client.beta.threads.runs.create_and_poll(
            thread_id = thread.id,
            assistant_id = assistant.id,
        )

        # What does the agent have to say?
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            #print(messages)
        else:
            print(run.status)
            print(run.last_error)

        # Return the data
        message_content = messages.data[0].content[0].text.value
        return self._response_to_dict(message_content)
    
    def _response_to_dict(self, message_content):
        print("Converting the following JSON to DICT:\n")
        print(f"\t\t{message_content}\n")
        
        # The slicing is to remove some random stuff from the OpenAI APIs
        # "```json" is 7 character long, but slicing count start from 0. "{" is at 7th character.
        # "```" is 3 character long (at the end).
        if message_content.startswith("```json") and message_content.endswith("```"):
            print("Slicing the response")
            message_content = message_content[7:-3]
        
        # Clean up the resultant JSON
        message_content = message_content.replace('\n', '')

        # Remove leading and trailing spaces in keys using regex
        message_content = re.sub(r'"\s*([^"]*?)\s*"\s*:', r'"\1":', message_content)
        
        # Finally, convert to dict and return
        return json.loads(message_content)

