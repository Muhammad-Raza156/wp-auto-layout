image_generation_prompt = """
To create this content, you must use the information provided to you in "BRAND STORY MAP" section as the contextual framework and the engine to write all the prompts to remake all the images for this section.

You can find JSON in the "JSON DATA" for a website page. Analyse the "JSON DATA" and extract all the images links. Also include the copywriting correlated with each image.

Ignore any images that are Logo's, do not include those links.

For these extracted image links, make a set of prompts to create new images using the "BRAND STORY MAP" as context to generate a phenomenal set of prompts for the new images to be created.

Create "alt-text" that simply describes what's in the image, using a maximum of 40 characters and "title" for all the extracted image links that will be for SEO purposes. 

And for the output, make a JSON in the below format and put all the original extracted image links in "extracted_image_links" and put all the new prompts in a "prompts" and similary alt-text in 
"alt_text" and "title" in "image_title". 

Create an alt text for each image that simply describes what's in the image, using a maximum of 40 characters

{{
    "extracted_image_links": [
        "https://www.example.com/image1.jpg",
        "https://www.example.com/image2.jpg",
        "https://www.example.com/image3.jpg",
        "https://www.example.com/image4.jpg",
        ...
        ...
    ],
    "prompts": [
        "Generate an image of a happy family with a baby in a park......",
        "Create an image of a happy couple walking on the beach.......",
        "Generate an image of a happy family with a baby in a park.....",
        "Create an image of a happy couple walking on the beach.....",
        ...
        ...
    ],
    "alt_text": [
        "Smiling family with baby in a sunny park, happy family, baby in a park.........",
        "Couple holding hands on a sandy beach, happy couple, walking on the beach.........",
        "Smiling family with baby in a sunny park, happy family, baby in a park"........,
        "Couple holding hands on a sandy beach, happy couple talking a walk on the beach..........",
        ...
        ...
    ],
    "image_title": [
        "baby-girl-baby-shower-gift",
        "picture-of-serious-businessman-standing",
        "cute-newborn-clothes-organic-cotton-baby-apparel",
        "Antonin-Scalia-Signature",
        ...
        ...
    ]  
}}
"""