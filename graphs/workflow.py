import operator
from typing import List, TypedDict, Annotated, Dict, Any

from langgraph.graph import StateGraph, START, END, add_messages
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_xai import ChatXAI
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image
from google import genai

from config.settings import GROQ_API_KEY, GEMINI_API_KEY, MODEL_NAME_GEMINI, MODEL_NAME_GROQ, GROK_API_KEY, GROK_MODEL_NAME
from prompts import (brand_story_questions, recap_intent_system_prompt, base_summary_prompt, bs_map_prompt,
                      summary_system_message, text_content_prompt_base, image_generation_prompt, home_page_system_prompt) 
from agents import (ask_question, summary_agent, human_node, summary_recap_intent, bs_map_agent, text_content,
                     create_img_content, home_page, wordpress_theme)


# Initialize your LLM (adjust parameters as needed)
llm_grok = ChatXAI(
    model=GROK_MODEL_NAME,
    api_key=GROK_API_KEY
)

client = genai.Client(api_key=GEMINI_API_KEY)

llm_gemini = ChatGoogleGenerativeAI(
    model=MODEL_NAME_GEMINI,
    api_key=GEMINI_API_KEY
    )

url="https://www.allbirds.com/?srsltid=AfmBOopnCLt7VtlnjnYo2RwW6k6mxo9jqsIAayMwWnF3O7Rt0asTtRtf"

# --- Define State ---
class ContentCreationState(TypedDict):
    responses: List[str]    # Collected answers  List[str]
    current_question_idx: int                   # Index of the current question
    summary: str                              # Last generated summary
    sum_recap_intent: str                     # User's intent on the summary recap
    questions: List[str]
    bs_map: str
    sections: str
    themes: Dict[str, Any]
    updated_page_content:str

# --- Build the State Graph ---
workflow = StateGraph(ContentCreationState)

# Add our three nodes.
workflow.add_node("ask_question", lambda state: ask_question(state, brand_story_questions))
workflow.add_node("human_node", lambda state: human_node(state))
workflow.add_node("summary_agent",  lambda state: summary_agent(state, llm_grok, base_summary_prompt, summary_system_message))
workflow.add_node("summary_recap_intent", lambda state: summary_recap_intent(state, llm_grok, recap_intent_system_prompt))
workflow.add_node("brand_story_map", lambda state: bs_map_agent(state, llm_grok, bs_map_prompt))
workflow.add_node("home_page", lambda state: home_page(state, client, url, MODEL_NAME_GEMINI))
workflow.add_node("wordpress_theme", lambda state: wordpress_theme(state, client, MODEL_NAME_GEMINI))
workflow.add_node("text_content", lambda state: text_content(state, llm_grok, text_content_prompt_base, "893.json"))
workflow.add_node("image_generation", lambda state: create_img_content(state, llm_grok, image_generation_prompt))


def after_human_node(state: ContentCreationState):
    if state["current_question_idx"] < 6:
        return "ask_question"
    elif state["current_question_idx"] == 6:
        return "summary_agent"
    elif state["current_question_idx"] == 7 and "redo" in state["sum_recap_intent"].lower():
        return "summary_agent"
    elif state["current_question_idx"] == 7:
        return "summary_recap_intent"
    elif state["current_question_idx"] == 8: 
        return "summary_agent"

def after_summary_agent(state:ContentCreationState):
    if state["current_question_idx"] == 6 or (state["current_question_idx"] == 7 and "redo" in state["sum_recap_intent"].lower()):
        return "ask_question"
    if state["current_question_idx"] == 8:
        return "brand_story_map"
    
workflow.add_edge(START, "ask_question")
workflow.add_edge("ask_question", "human_node")
workflow.add_conditional_edges("human_node", after_human_node)
workflow.add_conditional_edges("summary_agent", after_summary_agent)
workflow.add_edge("summary_recap_intent", "ask_question")
workflow.add_edge("brand_story_map", "home_page")
workflow.add_edge("home_page", "wordpress_theme")
workflow.add_edge("wordpress_theme", "text_content")
workflow.add_edge("text_content", "image_generation")
workflow.add_edge("image_generation", END)


graph = workflow.compile()
# graph = workflow.compile(checkpointer=MemorySaver())
#Image(graph.get_graph().draw_mermaid_png())


def run_workflow():
    config = {"recursion_limit": 100}
    initial_prompt = input("Enter your initial prompt (or press Enter to continue): ")
    state: ContentCreationState = {"summary": [],
                                   "responses": [],
                                   "questions": [],
                                    "current_question_idx": 0,
                                    "sum_recap_intent": "",
                                    "bs_map": "",
                                    "updated_page_content":"",
                                    "sections":"",
                                    "themes":{}
                                }
    
    
    for event in graph.stream(state, config=config):
        if state.get("current_question_idx") == 8:
            print("\nWorkflow complete.")
            exit(0)

if __name__ == "__main__":
    run_workflow()
