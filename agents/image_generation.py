import os
import requests
import json
import fal_client

from PIL import Image
from io import BytesIO
from utils import read_json_as_text, find_and_replace    
from wordpress_utils import upload_image 

from dotenv import load_dotenv


load_dotenv()


WP_API_BASE_URL=os.environ.get("WP_API_BASE_URL", "")  
WP_USERNAME=os.environ.get("WP_USERNAME", "")                      
WP_APP_PASSWORD=os.environ.get("WP_APP_PASSWORD", "")

imgs_directory = "output_images"
os.makedirs(imgs_directory, exist_ok=True)

json_schema = {
    "title": "LLMGeneratedContent",
    "description": "Extract image links nad create new prompts, alt-text and title for the images.",
    "type": "object",
    "properties": {
        "extracted_image_links": {
            "type": "array",
            "description": "List of extracted image links from the JSON.",
            "items": {
                "type": "string",
                "description": "A specific image link extracted from the original JSON."
            }
        },
        "prompts": {
            "type": "array",
            "description": "List of new prompts to generate the images.",
            "items": {
                "type": "string",
                "description": "A new prompt version of the original text for the image."
            }
        },
        "alt_text": {
            "type": "array",
            "description": "List of alt-text for the extracted image links",
            "items": {
                "type": "string",
                "description": "A alt-text for the image link"
            }
        },
        "image_title": {
            "type": "array",
            "description": "List of titles for the extracted image links",
            "items": {
                "type": "string",
                "description": "A title for the image link"
            }
        }

    },
    "required": ["extracted_image_links", "prompts", "alt_text", "image_title"]
}


def create_img_content(state, llm, image_generation_prompt):
    brand_story_map = state["bs_map"]
            
    messages = [
        ("system", image_generation_prompt),
        ("human", f"Please do as described to you.  \n\n 'BRAND STORY MAP': \n{brand_story_map} \n\n 'JSON DATA': \n {state['updated_page_content']}"),
    ]
    structured_llm = llm.with_structured_output(json_schema)
    llm_output = structured_llm.invoke(messages)

    with open("image_generation_output.json", "w") as f:
        json.dump(llm_output, f)

    # Generate images using Flux schnell provided by FAL.AI
    generated_img_urls = [generate_image(prompt)
                            for prompt in llm_output["prompts"]]
    
    # Improvement: Directly pass in memory data to media library function to upload
    img_local_paths = [save_img_locally(img, f"{imgs_directory}/{image_title}.jpg")
                            for img, image_title in zip(generated_img_urls, llm_output["image_title"])]
    
    uploaded_img_urls =  [upload_image(WP_API_BASE_URL, img_path, WP_USERNAME, WP_APP_PASSWORD) 
                          for img_path in img_local_paths] 
    
    replacements = dict(zip([url.replace("/", r"\/") for url in llm_output["extracted_image_links"]], uploaded_img_urls))
    # Replace existing image urls with new generate ones 
    updated_content = find_and_replace(state["updated_page_content"], replacements)
    # Write modified content to a new file
    updated_json = json.loads(updated_content)
    
    with open("893_updated.json", "w") as file:
        json.dump(updated_json, file)
    return state

def generate_image(prompt):
    result = fal_client.subscribe("fal-ai/flux/schnell",
                                  arguments={"prompt": prompt},
                                  with_logs=True,
                                  on_queue_update=on_queue_update,)
    return result["images"][0]["url"]

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

def save_img_locally(image_url, img_output_path):
    # Save the image to the local directory
    """Fetches an image from a URL and returns the image object and size."""
    response = requests.get(image_url)
    
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(img_output_path)
        return img_output_path
    else:
        print("Failed to fetch the image.")
        return None
