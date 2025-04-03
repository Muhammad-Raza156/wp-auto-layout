def human_node(state):
    """
    Collect the user's answer and record it
    """
    answer = input()
    state["responses"].append(answer)
    return state
