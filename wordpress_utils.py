import os
import requests
from requests.auth import HTTPBasicAuth

def upload_image(api_base_url, image_path, username, app_password):
    """
    Uploads an image to the WordPress media library and returns the JSON response.
    """
    upload_endpoint = f"{api_base_url}/wp-json/wp/v2/media"
    # Set headers: The Content-Disposition header tells WordPress the filename.
    headers={ 'Content-Type': 'image/jpg','Content-Disposition' : f'attachment; filename=""{os.path.basename(image_path)}"'}
    # Read the image binary
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
    
    # Use basic authentication with your username and application password.
    response = requests.post(
        upload_endpoint,
        headers=headers,
        data=img_data,
        auth=HTTPBasicAuth(username, app_password)
    )
    
    if response.status_code in (200, 201):
        resp_json = response.json()
        uploaded_img_url = resp_json.get("source_url")
        print("Uploaded image URL:", resp_json.get("source_url"))
        return uploaded_img_url
    else:
        print("Error uploading image:", response.status_code, response.text)
        return None

def get_all_media_urls(api_base_url, username, app_password, per_page=100):
    """
    Retrieves all media items from the WordPress media library and extracts their URLs.
    """
    media_endpoint = f"{api_base_url}/wp-json/wp/v2/media"
    page = 1
    all_urls = []
    
    while True:
        params = {"per_page": per_page, "page": page}
        response = requests.get(
            media_endpoint,
            params=params,
            auth=HTTPBasicAuth(username, app_password)
        )
        
        if response.status_code != 200:
            print("Error fetching media:", response.status_code, response.text)
            break
        
        items = response.json()
        if not items:
            break  # No more items on this page
        
        # Extract the source_url for each media item
        for item in items:
            url = item.get("source_url")
            if url:
                all_urls.append(url)
        print(f"Fetched page {page} with {len(items)} items.")
        page += 1

    return all_urls

