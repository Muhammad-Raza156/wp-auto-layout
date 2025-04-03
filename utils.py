import json
import requests
from PIL import Image
from io import BytesIO
import re


def read_json_as_text(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return file.read()
    
def save_json(file_path, data):
    """Saves JSON to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def find_and_replace(page_content, replacements):
    """
    Reads a file, replaces occurrences of original content with rewritten content, and writes to a new file.
    """
    # Replace occurrences of original text with rewritten text
    for original, rewritten in replacements.items():
        page_content = page_content.replace(original, rewritten)    
    return page_content

def fetch_image_info(url):
    """Fetches an image from a URL and returns the image object and size."""
    response = requests.get(url)
    
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        size_kb = len(response.content) / 1024  # Convert to KB
        
        print(f"Original Dimensions: {width}x{height}")
        print(f"Original File Size: {size_kb:.2f} KB")
        
        return width, height, size_kb
    else:
        print("Failed to fetch the image.")
        return None, None, None, None

def compress_image(img, max_size_kb=100, quality=85):
    """Compress the image while keeping the same dimensions until it fits within max_size_kb."""
    output = BytesIO()
    
    img.save(output, format="JPEG", quality=quality)
    size_kb = len(output.getvalue()) / 1024  # Get compressed size in KB
    
    while size_kb > max_size_kb and quality > 10:
        quality -= 5
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality)
        size_kb = len(output.getvalue()) / 1024
    
    print(f"Compressed File Size: {size_kb:.2f} KB with quality {quality}")
    return Image.open(output)  # Return compressed image

def clean_html(html_content):
    # Remove <head> tag and its content
    html_content = re.sub(r'<head.*?>.*?</head>', '', html_content, flags=re.DOTALL)

    # Remove <style> tag and its content
    html_content = re.sub(r'<style.*?>.*?</style>', '', html_content, flags=re.DOTALL)

    # Remove <script> tag and its content
    html_content = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)

    # Remove <svg> tag and its content
    html_content = re.sub(r'<svg.*?>.*?</svg>', '', html_content, flags=re.DOTALL)

    # Remove <img> tags (self-closing)
    html_content = re.sub(r'<img.*?>', '', html_content, flags=re.DOTALL)

    return html_content