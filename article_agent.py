from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langgraph.prebuilt import create_react_agent
from flask import url_for
import uuid

def build_toolchain():
    search = TavilySearchResults(max_results=1)

    # Put all the tools into a list to reference later.
    tools = []
    tools.append(search)

    toolkit = RequestsToolkit(
        requests_wrapper=TextRequestsWrapper(headers={}),
        allow_dangerous_requests=True,
    )

    for t in toolkit.get_tools():
        tools.append(t)

    print("Available tools:")
    for t in tools:
        print(t)

    return tools

def get_agent():
    # Initialize the model
    model = ChatOpenAI(model="gpt-4o-mini")

    # Initialize the memory
    memory = MemorySaver()

    # Build out the toolchain
    tools = build_toolchain()

    system_prompt = "You are an expert eCommerce content writer focused on creating compelling, informative, and SEO-optimized long form shopping articles. Write engaging content that highlights product features, benefits, and unique selling points, aiming to educate and persuade potential buyers. Your tone should be friendly, professional, and tailored to the brand’s target audience. Prioritize clarity, accuracy, and readability. You are to present helpful and reliable information that's primarily created to benefit people, not to gain search engine rankings, so that the content naturally rises into the top Search results."

    # Initialize the agent
    agent_executor = create_react_agent(model, tools, checkpointer=memory, state_modifier=system_prompt)
    return agent_executor

def write(catalog_item):
    agent = get_agent()

    product_link = url_for('catalog_pdp', id=catalog_item.id, _external=True)
    #For testing. Need an absolute link for the model to access the content.
    #product_link = f"https://flask-hello-world-n1hj.onrender.com/catalog/pdp?id={catalog_item.id}"
    print(f"Generating product article using product_link: {product_link}")

    user_prompt = f"""
    You are to write a long form article to promote the following product.

    URL: {product_link}

    The following are steps I want you to take:
    1. Identify the product based on its URL. We'll refer to this as the input product.
    2. Search for competing products in the same category to compare the input product against.
    3. From the search results, identify the top 2 products that are most similar to the input product.
    4. Write a long form article to promote the product. Include the following sections: Introduction, Overview of Products, Product Feature Comparison, Pricing, Final Recommendation.
    5. In the Final Recommendation, include a call-to-action to purchase the input product, which links back to the URL above.

    The following are guardrails that I want you to stay within:
    1. The article should be engaging, informative, and SEO-optimized.
    2. The article must include a table in the Product Feature Comparison section to showcase the products side-by-side, with images where available, and highlighting key features.
    3. The article must compare a minimum of 3 products, inclusive of the input product.
    4. The article must include images of the mentioned products. When images are not available, use the following as the image source instead: https://placehold.co/100

    The output article is to be in HTML format. Include nothing else, no pre-amble, no explanations. Output only the HTML that is valid and proper such that it can be rendered directly.
    """

    inputs = {"messages": [("user", user_prompt)]}

    # Create a UUID to identify the specific session with memory
    thread_id = str(uuid.uuid4())
    print(f"Using THREAD_ID: {thread_id}")
    config = {"configurable": {"thread_id": thread_id}}

    # This is a blocking synchronous call
    response = agent.invoke(inputs, config)
    # Get the last element from the response
    message_content = response['messages'][-1].content

    # The slicing is to remove some random stuff from the OpenAI APIs
    # "```html" is 7 character long, but slicing count start from 0. "{" is at 7th character.
    # "```" is 3 character long (at the end).
    if message_content.startswith("```html") and message_content.endswith("```"):
        print("Slicing the response")
        message_content = message_content[7:-3]

    return message_content