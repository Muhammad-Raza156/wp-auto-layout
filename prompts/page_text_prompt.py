text_content_prompt_base = """
You are the world's best content generator tasked with creating high-quality, conversion rate optimization, storytelling focused copywriting for landing pages,
funnels and websites for products and services. These landing pages, funnels and websites need to be specifically tailored for lead generation and ecommerce sales.

To write this content, you must use the information from the "BRAND STORY MAP" as the contextual framework and
the engine to rewrite all the specific copywriting content for the page.

Step 1:
You can find JSON in the "JSON DATA" for a website page. It has code for building a page in elementor page builder. It has written content I want to isolate and extract from the JSON. Can you list all the copywriting text from this JSON into a bullet pointed list.

Step 2:
Then use the "BRAND STORY MAP" to rewrite the copy using exactly the same content list from the json in Step 1. Keep the character count roughly the same give or take 20%.
And for the output, make a JSON in the below format and put all the original text in "original_content" and the new text in a "rewritten_content".

Return the the valid JSON format as follows:


{{
  "original_content": [
    "About us",
    "Welcome to our baby shop: one-stop-shop for all your baby needs!",
    ...
    ...
  ],
  "rewritten_content": [
    "About Happy Humans",
    "Unlock Your Full Potential:  Your Partner in Peak Performance"
    ...
    ...
  ]
}}

"""


# text_content_prompt_base = """
# You are the world's best content generator tasked with creating high-quality, conversion rate optimization, storytelling focused copywriting for landing pages,
# funnels and websites for products and services. These landing pages, funnels and websites need to be specifically tailored for lead generation and ecommerce sales.

# To write this content, you must use the information from the "BRAND STORY MAP" as the contextual framework and
# the engine to rewrite all the specific copywriting content for the page.

# Step 1:
# You can find JSON in the "JSON DATA" for a website page. It has code for building a page in elementor page builder. It has written content I want to isolate and extract from the JSON. Can you list all the copywriting text from this JSON into a bullet pointed list.

# Step 2:
# Then use the "BRAND STORY MAP" to rewrite the copy using exactly the same content list from the json in Step 1. Keep the character count roughly the same give or take 20%.
# And for the output, make a table and put the original text in one column and the new text in a new column next to it, side by side. 
# """


# Happy Humans
# Happy Human Daily Supplements
# Take one pill per day and feel your very best and conquer the day
# Pills to make humans happier more driven and gives a heightened mental state every day to help you crush your goals
# Anyone 30+ men and women who are high achievers 
# It is really taking off for people who want to have enhanced cognitive abilities and life longevity



