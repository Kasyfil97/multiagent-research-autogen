import autogen
from typing_extensions import Annotated
from apify_client import ApifyClient
from config import Config
import requests
import json
from agents import user, manager, researcher, analyst, spokesman, executor
from config import Config, API_KEYS

config = Config.load_yaml()
api_keys = API_KEYS.load_env()

@executor.register_for_execution()
@researcher.register_for_llm(description="web scrapping")
def scrape_page(url: Annotated[str, "The URL of the web page to scrape"]) -> Annotated[str, "Scraped content"]:
    # Initialize the ApifyClient with your API token
    client = ApifyClient(token=api_keys.apify_api_key)

    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "useSitemaps": False,
        "crawlerType": "playwright:firefox",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "ignoreCanonicalUrl": False,
        "maxCrawlDepth": 0,
        "maxCrawlPages": 1,
        "initialConcurrency": 0,
        "maxConcurrency": 200,
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "maxSessionRotations": 10,
        "maxRequestRetries": 5,
        "requestTimeoutSecs": 60,
        "dynamicContentWaitSecs": 10,
        "maxScrollHeightPixels": 5000,
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "removeCookieWarnings": True,
        "clickElementsCssSelector": '[aria-expanded="false"]',
        "htmlTransformer": "readableText",
        "readableTextCharThreshold": 100,
        "aggressivePrune": False,
        "debugMode": True,
        "debugLog": True,
        "saveHtml": True,
        "saveMarkdown": True,
        "saveFiles": False,
        "saveScreenshots": False,
        "maxResults": 9999999,
        "clientSideMinChangePercentage": 15,
        "renderingTypeDetectionPercentage": 10,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)

    if run.get("status") == "SUCCEEDED":

        # Fetch and print Actor results from the run's dataset (if there are any)
        text_data = ""
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            text_data += item.get("text", "") + "\n"

        average_token = 0.75
        max_tokens = 20000  # slightly less than max to be safe 32k
        text_data = text_data[: int(average_token * max_tokens)]
    else:
        print(f"HTTP request failed with status code {run.get('status')}") 

    return text_data

# Function for google search
@executor.register_for_execution()
@researcher.register_for_llm(description="search information by google api")
def google_search(
    search_keyword: Annotated[str, "the keyword to search information by google api"]) -> Annotated[dict, "the json response from the google search api"]:
    """
    Perform a Google search using the provided search keyword.

    Args:
    search_keyword (str): The keyword to search on Google.

    Returns:
    str: The response text from the Google search API.
    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": search_keyword
    })

    headers = {
    'X-API-KEY': api_keys.serper_api_key,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE:", response.text)
    return response.text


# Function for google search
@executor.register_for_execution()
@researcher.register_for_llm(description="search location by google maps api")
def google_maps_search(
    keyword: Annotated[str, "the keyword to search location"]) -> Annotated[dict, "the json response from the google maps api"]:
    """
    Perform a Google search using the provided search keyword.

    Args:
    search_keyword (str): The keyword to search on Google.

    Returns:
    str: The response text from the Google search API.
    """
    url = "https://google.serper.dev/maps"

    payload = json.dumps({
    "q": keyword
    })

    headers = {
    'X-API-KEY': api_keys.serper_api_key,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE:", response.text)
    return response.text


def main(message):
    groupchat = autogen.GroupChat(
        agents=[user, manager, researcher, analyst, spokesman, executor],
        messages=[],
        max_round=20,
        speaker_selection_method="auto"  # Ensuring each agent speaks in turn
    )
    chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=config.gpt4_config)
    user.initiate_chat(
        chat_manager,
        message=message,
    )

if __name__ == "__main__":
    message = input("Enter your message: ")
    main(message)