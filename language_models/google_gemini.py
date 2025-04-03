from langchain_google_genai import ChatGoogleGenerativeAI

def run_gemini_model(gemini_api_key : str, model_name_gemini : str, human_message : str, system_message: str):
    llm_gemini = ChatGoogleGenerativeAI(
        model=model_name_gemini,
        google_api_key=gemini_api_key
    )

    messages = [
            ("system", system_message),
            ("human", human_message),
        ]

    response = llm_gemini.invoke(messages).content
    return response
    