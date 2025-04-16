import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class PerformanceMetrics(BaseModel):
    page_speed_score: float = Field(..., ge=0, le=100)
    mobile_responsiveness: bool
    seo_optimization: bool

class CustomizationPotential(BaseModel):
    elementor_compatibility: bool
    color_customization: bool
    layout_flexibility: float = Field(..., ge=0, le=100)

class RecommendedTheme(BaseModel):
    theme_name: str
    theme_id: str
    overall_match_score: float = Field(..., ge=0, le=100)
    features: List[str]
    layout_match_score: float = Field(..., ge=0, le=100)
    brand_story_match_score: float = Field(..., ge=0, le=100)
    match_reason: str
    performance_metrics: PerformanceMetrics
    customization_potential: CustomizationPotential

class ThemeRecommendation(BaseModel):
    recommended_themes: List[RecommendedTheme]
    recommendation_methodology: str

def wordpress_theme(state, client, model_name):
    """
    Recommends WordPress themes based on a brand story map and a webpage's HTML structure.

    This function analyzes a brand's identity and a webpage's layout to suggest
    WordPress themes that align with both the brand's narrative and the webpage's
    design. It uses a language model to evaluate potential themes against
    criteria such as design layout matching, brand story alignment, technical
    requirements, and customization capabilities.

    Args:
        state (dict): The current state of the workflow, containing:
            - "bs_map" (str): The brand story map.
            - "sections" (str): The HTML structure description of the webpage.
        client: An instance of a language model client, configured for text generation.
                This client is used to interact with the language model to analyze
                the brand story map and HTML content.
        model_name (str): The name of the language model to use for analysis.

    Returns:
        dict: The updated state dictionary, with the "themes" key containing a
              list of recommended WordPress themes, formatted as a JSON object.
    """

    bsmap_content= state["bs_map"]
    sections = state["sections"]

    theme_prompt= f"""
        You are a world-class WordPress theme expert. Your task is to recommend WordPress themes that closely match a given **webpage layout** while ensuring they align with the brand's identity and storytelling.

        ## Context:
        - Provided: **Section-wise HTML structure description** of a webpage
        - Provided: **Brand Story Map** containing brand's purpose, target audience, core message, brand personality, and call-to-action
        - Goal: **Match structure and storytelling elements** with existing WordPress themes

        ## Comprehensive Evaluation Criteria:
        ### Design Layout Matching
        1. Structural Alignment
        - Header configuration
        - Section layouts
        - Responsive design
        - Navigation patterns

        ### Brand Story Alignment
        1. Visual Storytelling Elements
        - Color psychology
        - Typography matching brand personality
        - Emotional design resonance
        - Storytelling section capabilities

        ### Technical Requirements
        1. Performance Metrics
        - Page load speed
        - Mobile responsiveness
        - SEO optimization
        2. Customization Capabilities
        - Elementor compatibility (High Priority)
        - Flexibility in section designs
        - Color and typography customization

        ## Recommendation Instructions:
        1. Analyze HTML structure description for layout intricacies
        2. Deeply evaluate Brand Story Map for storytelling alignment
        3. Select themes matching both design and brand narrative
        4. Prioritize Elementor-compatible themes
        5. Generate JSON output with comprehensive theme insights


        ## Recommendation Guidelines:
        - Minimum 3, Maximum 5 theme recommendations
        - Themes must have at least 4/5 star rating
        - Preference for themes with active development and support
        - Consider themes from reputable marketplaces (ThemeForest, StudioPress, etc.)

        ## Scoring Methodology:
        - Layout Match (40%): Structural similarity
        - Brand Story Match (30%): Narrative and emotional alignment
        - Performance (15%): Technical capabilities
        - Customization (15%): Flexibility and adaptability

        ## Input Sections:
        ### HTML Structure Description:
        {sections}

        ### Brand Story Map:
        {bsmap_content}

        ## Output JSON Structure:
        ```json
        {{
        "recommended_themes": [
            {{
            "theme_name": "String",
            "theme_id": "String",
            "overall_match_score": "Float (0-100)",
            "features": ["Array of Features"],
            "layout_match_score": "Float (0-100)",
            "brand_story_match_score": "Float (0-100)",
            "match_reason": "Detailed explanation of theme selection",
            "performance_metrics": {{
                "page_speed_score": "Float (0-100)",
                "mobile_responsiveness": "Boolean",
                "seo_optimization": "Boolean"
            }},
            "customization_potential": {{
                "elementor_compatibility": "Boolean",
                "color_customization": "Boolean",
                "layout_flexibility": "Float (0-100)"
            }}
            }}
        ],
        "recommendation_methodology": "Detailed explanation of selection process"
        }}
        ```
        """
    response= client.models.generate_content(
        model=model_name,
        contents=theme_prompt,
        config={'response_mime_type': 'application/json',
        'response_schema': ThemeRecommendation}
    )

    themes=response.text
    print(themes)
    #state["themes"]=json.loads(themes)
    state["themes"]=themes
    return state
