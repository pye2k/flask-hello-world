from openai import OpenAI
import json

def go(input):
    client = OpenAI()

    # Retrieve the handle to the "E-Commerce Catalog Enrichment Agent"
    assistant = client.beta.assistants.retrieve("asst_hybknDl6aMxaEgD8x7ruLP4W")

    # Create a thread (a conversation between user and agent)
    thread = client.beta.threads.create()

    # Add a message to the Thread (from the user)
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = input
        )

    # Get the agent to do the work
    instructions = """
    Generate a product title, short description, and detailed description for this product.

    - The title should be concise and relevant to the category, prioritizing for readability, keyword searches via SEO.
    - The short description should provide a concise summary of the product, prioritizing the key features relevant for SEO and attraction to a human reader.
    - The detailed description should provide a clear and informative overview of the product. Aim for approximately 200 words.

    Additionally, include a list of relevant specifications in JSON format. For exmaple:
    "specifications": [
        {"name": "Color", "value": "Red"},
        {"name": "Material", "value": "Cotton"},
        {"name": "Weight", "value": "1 kg"}
    ]

    Return the data in JSON format with the keys "title", "short_description", "detailed_description", and "specifications".
    """

    # Create a run, and poll for completion
    run = client.beta.threads.runs.create_and_poll(
        thread_id = thread.id,
        assistant_id = assistant.id,
        instructions = instructions
        )

    # What does the agent have to say?
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        #print(messages)
    else:
        print(run.status)

    # Return the data
    message_content = messages.data[0].content[0].text.value
    print("Response: \n")
    print(f"{message_content}\n\n")

    # The slicing is to remove some random stuff from the OpenAI APIs
    # "```json" is 7 character long, but slicing count start from 0. "{" is at 7th character.
    # "```" is 3 character long (at the end).
    return message_content[7:-3]

def interweave(short_description, search_query):
    client = OpenAI()

    # Retrieve the handle to the "Search Query Interweaver" Assistant
    assistant = client.beta.assistants.retrieve("asst_guPYqtgOFMO8T7gNVydJuFdz")

    # Create a thread (a conversation between user and agent)
    thread = client.beta.threads.create()

    # Create an object with the short_description and search_query
    input_object = {
        "text_block": short_description,
        "search_query": search_query
    }

    # Add a message to the Thread (from the user)
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = json.dumps(input_object)
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

    # Return the data
    message_content = messages.data[0].content[0].text.value
    print("Response: \n")
    print(f"{message_content}\n\n")
    return message_content