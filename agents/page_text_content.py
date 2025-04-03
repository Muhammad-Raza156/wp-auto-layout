import os
import json
from utils import read_json_as_text, find_and_replace 

json_schema = {
    "title": "LLMGeneratedContent",
    "description": "Extracted and rewritten content from LLM for website copywriting.",
    "type": "object",
    "properties": {
        "original_content": {
            "type": "array",
            "description": "List of extracted original text content from the JSON.",
            "items": {
                "type": "string",
                "description": "A specific text extracted from the original JSON."
            }
        },
        "rewritten_content": {
            "type": "array",
            "description": "List of rewritten text content based on BRAND STORY MAP.",
            "items": {
                "type": "string",
                "description": "A rewritten version of the original text."
            }
        }
    },
    "required": ["original_content", "rewritten_content"]
}


def text_content(state, llm, text_content_prompt_base, json_file_path):
    """
    Generate a text content based on collected responses using the LLM
    """
    page_json_content = read_json_as_text(json_file_path)
    brand_story_map = state["bs_map"]
            
    messages = [
        ("system", text_content_prompt_base),
        ("human", f"Please create text content as described to you.  \n\n 'BRAND STORY MAP': \n{brand_story_map} \n\n 'JSON DATA': \n {page_json_content}"),
    ]

    structured_llm = llm.with_structured_output(json_schema)
    text_content = structured_llm.invoke(messages)
    print("-----------------text content-----------------")
    print(text_content)    
    replacements = dict(zip(text_content["original_content"], text_content["rewritten_content"]))
    
    # Find the orignal content and replace it with the rewritten content
    updated_content = find_and_replace(page_json_content, replacements)
    state["updated_page_content"] = updated_content 

    print("--------Text content generated and updated in the JSON-----------")
    return state
