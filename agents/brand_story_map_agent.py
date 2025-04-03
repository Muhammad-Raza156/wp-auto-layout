def bs_map_agent(state, llm, base_prompt):
    """Generate a brand story map on collected responses from the user."""
    brand_story_main_prompt = f"""Here are the answers from the user: \n{state["summary"]}\n\n {base_prompt}"""    

    messages = [
        ("system", brand_story_main_prompt),
        ("human", f"Please create brand story map as described to you. \n Here are the users answers: {state['summary']}"),
    ]
    brand_story_map = llm.invoke(messages).content
    
    file_path = "brand_story_map.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(brand_story_map)
    state["bs_map"] = brand_story_map
    print("Brand story map generated")
    return state
