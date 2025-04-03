
def summary_agent(state, llm, user_summary_prompt, summary_system_message):
    """
    Generate a summary based on collected responses using the LLM
    """
    question_and_answers = list(zip(state["questions"], state["responses"]))
    
    for question, answer in question_and_answers:
        user_summary_prompt += f"Question: {question}\nAnswer: {answer}\n\n"

    
    messages = [
        ("system", summary_system_message),
        ("human", user_summary_prompt),
        ]

    # response = llm.invoke([{"role": "user", "content": summary_prompt_base}])
    response = llm.invoke(messages)
    summary_text = response.content
    state["summary"] = summary_text
    print(summary_text)
    return state
