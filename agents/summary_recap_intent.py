def summary_recap_intent(state, llm, recap_intent_system_prompt):
    """Check if the user accepts the summary recap."""
    last_answer = state["responses"][-1] if state["responses"] else ""

    recap_prompt = f"\nUser answer is this: {last_answer}"

    messages = [
        ("system", recap_intent_system_prompt),
        ("human", f"Please check the intent on this answer: {recap_prompt}"),
        ]

    # Call the LLM – adjust response access if needed.
    # response = llm.invoke([{"role": "user", "content": recap_prompt}])
    response = llm.invoke(messages)
    user_recap_intent = response.content
    state["sum_recap_intent"] = user_recap_intent
    return state
