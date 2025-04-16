def human_node(state, answer=""):
    """
    Collect the user's answer and record it
    """
    print("i am at human node ")
    if len(state["responses"]) < len(state["questions"]):
        state["responses"].append(answer)
    return state
