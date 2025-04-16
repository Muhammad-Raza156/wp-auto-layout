from utils import clean_html
import requests
import asyncio
import time
def home_page(state, client, model_name):
    """
    Analyzes the HTML content of a given URL to identify and describe key sections of a website's home page.

    This function fetches the HTML content of a specified URL, cleans it by removing
    unnecessary tags (like <head>, <style>, <script>, and <svg>), and then uses a
    language model to analyze the cleaned HTML. The language model identifies key
    sections within the HTML and provides a text description of each section,
    including layout structure, position, sub-sections, and overall design information.

    Args:
        state (dict): The current state of the workflow, which is a dictionary.
                      This dictionary is expected to be updated with the extracted
                      sections under the key "sections".
        client: An instance of a language model client, configured for text generation.
                This client is used to interact with the language model to analyze
                the HTML content.
        url (str): The URL of the website to analyze.
        model_name (str): The name of the language model to use for analysis.

    Returns:
        dict: The updated state dictionary, with the "sections" key containing a string
              describing the identified sections of the home page.
    """
    print(f"\n\n==== HOME PAGE AGENT ====")
    print(f"Url in state: {state['url']}")
    print(f"Summary intent: {state['sum_recap_intent']}")
    time.sleep(0.1)

    # DEBUG: Add breakpoint before checking URL
    #import pdb; pdb.set_trace()  # Breakpoint 5: Before checking URL in home_page_agent

    if not state["url"]:
        #url = "https://www.allbirds.com/?srsltid=AfmBOopnCLt7VtlnjnYo2RwW6k6mxo9jqsIAayMwWnF3O7Rt0asTtRtf"
        print("URL in state is empty, using default URL")
        state["url"]="https://www.allbirds.com/?srsltid=AfmBOopnCLt7VtlnjnYo2RwW6k6mxo9jqsIAayMwWnF3O7Rt0asTtRtf"
    else:
        print(f"Using URL from state: {state['url']}")

    url=state["url"]
    print(f"Final URL being used: {url}")
    response = requests.get(url)
    html_content = response.text
    html_content = clean_html(html_content)

    user_prompt = f"""
    **Html Content**
    {html_content}

    **Html Content** provided above is landing page of a website.
    Modern websites are designed in such a way that their landing or home page mostly contains 4 to 13 major or key sections.
    Number of sections can vary, but normally between 4 to 13.

    Your task is to identify key sections in the **Html Content**.
    In response a dictionary where key will be the section name and value will be text description of that section.
    Text description of the section shall contain, layout structure information, its position, other sub-sections in it and overall design and structer information.
    No extra text in the response.

    Ensure that the extracted sections maintain their web-friendly formatting.
    """
    response= client.models.generate_content(
        model=model_name,
        contents=user_prompt,
    )
    sections = response.text.strip()
    state["sections"]=sections
    print(sections)
    return state