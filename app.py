import streamlit as st
from graphs.workflow import run_workflow, ContentCreationState, graph
import time

def display_state(state: ContentCreationState):
    """Displays the current state in the sidebar."""
    st.sidebar.header("Current State")
    for key, value in state.items():
        st.sidebar.write(f"**{key}:** {value}")


def main():
    st.title("Automated Content Creation")

    if "state" not in st.session_state:
        st.session_state.state = {"summary": [],
                                   "responses": [],
                                   "questions": [],
                                   "current_question_idx": 0,
                                   "sum_recap_intent": "",
                                   "bs_map": "",
                                   "updated_page_content": "",
                                   "sections": "",
                                   "themes": {}}
        st.session_state.config = {"recursion_limit": 100}
        st.session_state.workflow_started = False
        st.session_state.events = []

    display_state(st.session_state.state)

    if not st.session_state.workflow_started:
        st.write("Welcome! Let's start creating your website landing page.")
        if st.button("Start"):
            st.session_state.workflow_started = True
            # Add the first question to the state
            # for event in graph.stream(st.session_state.state, config=st.session_state.config):
            #     st.session_state.events.append(event)
            #     if st.session_state.state.get("current_question_idx", 0) == 1:
            #         st.session_state.state["questions"].append(st.session_state.events[0].get("state").get("questions")[0])
            #         break
            next(graph.stream(st.session_state.state, config=st.session_state.config))
            st.rerun()

    if st.session_state.workflow_started:
        if st.session_state.state.get("current_question_idx", 0) < 8:
            current_question_idx = st.session_state.state.get("current_question_idx", 0)
            if current_question_idx < len(st.session_state.state["questions"]):
                question = st.session_state.state["questions"][current_question_idx]
                st.write(f"**Question {current_question_idx + 1}:** {question}")
            else:
                for event in graph.stream(st.session_state.state, config=st.session_state.config):
                    st.session_state.events.append(event)
                    if st.session_state.state.get("current_question_idx", 0) > current_question_idx:
                        st.session_state.state["questions"].append(st.session_state.events[-1].get("state").get("questions")[-1])
                        break
                    if st.session_state.state.get("current_question_idx", 0) == 8:
                        break
                st.rerun()
            user_response = st.text_area("Your Response:", key=f"response_{current_question_idx}")
            if st.button("Submit Response"):
                st.session_state.state["responses"].append(user_response)
                next(graph.stream(st.session_state.state, config=st.session_state.config))
                st.rerun()
        else:
            st.write("Workflow complete.")
            st.write("## Summary")
            st.write(st.session_state.state["summary"])
            st.write("## Brand Story Map")
            st.write(st.session_state.state["bs_map"])
            st.write("## Home Page Analysis")
            st.write(st.session_state.state["sections"])
            st.write("## Theme Recommendations")
            st.write(st.session_state.state["themes"])
            st.write("## Updated Page Content")
            st.write(st.session_state.state["updated_page_content"])
            st.write("## Events")
            st.write(st.session_state.events)

if __name__ == "__main__":
    main()
