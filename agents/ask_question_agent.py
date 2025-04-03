def ask_question(state, brand_story_questions):
    """Ask one pre-defined question and record"""
    q_index = state["current_question_idx"]
    
    # Remove 7 condtion if simple does not work - and state["current_question_idx"] == 7
    if q_index < len(brand_story_questions):
        if  "redo" in state["sum_recap_intent"].lower() and len(state["responses"])<8:
            question = "Okay, please make any changes you'd like to the summary."
            state["questions"].append(question)
        else: # Support no summary recap condition here   
            question = brand_story_questions[q_index]
            state["current_question_idx"] += 1
            state["questions"].append(question)
        print(question)
    return state



# ""Ask one pre-defined question and record"""
#     q_index = state["current_question_idx"]
#     # Remove 7 condtion if simple does not work - and state["current_question_idx"] == 7
#     if q_index < len(brand_story_questions):
#         if  "redo" in state["sum_recap_intent"].lower():
#             question = "Okay, please make any changes you'd like to the summary."
#             state["questions"].append(question)
#         else: # Support no summary recap condition here   
#             question = brand_story_questions[q_index]
#             state["current_question_idx"] += 1
#             state["questions"].append(question)
#         print(question)
# """