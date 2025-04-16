from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from langgraph.pregel import GraphRecursionError
from graphs.workflow import graph, ContentCreationState


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def say_hello():
    return {"message": f"application is up and running"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Establishing websocket connection")
    await websocket.accept()
    print("WebSocket connection accepted")

    state: ContentCreationState = {
    "summary": [],
    "responses": [],
    "questions": [],
    "current_question_idx": 0,
    "sum_recap_intent": "",
    "bs_map": "",
    "updated_page_content":"",
    "url":"",
    "sections":"",
    "themes":{}
    }
    # url=""
    # if not url:
    #     url_msg= "Give the url of website home page for which analysis will be performed"
    #     await websocket.send_json({"type":"request_url",
    #                                                 "payload":url_msg})
    #     data = await websocket.receive_json()
    #     messgae_type= data.get("type")
    #     payload = data.get("payload")
    #     if messgae_type == "send_url" and payload and payload.strip(): # Check type and non-empty payload
    #             print(f"Received URL: {payload}")
    #             # DEBUG: Add breakpoint here to track URL reception in main.py
    #             import pdb; pdb.set_trace()  # Breakpoint 3: URL received in main.py
    #             url = payload.strip()
    #             print(f"URL variable set to: {url}")

    try:
        print("Starting workflow stream")
        async for event in graph.astream(state, {"recursion_limit" : 100}):
                print(f"--- Raw Event Received: {event} ---")
                node_name = next(iter(event))
                print(f"Processing node: {node_name}")
                new_state_values = event[node_name]
                #new_state_values["url"] = url
                state.update(new_state_values)
                #state["url"]=url

                print(f"Initial graph event processed. State: {state}")
                q_index=state["current_question_idx"]

                if q_index < 6 and node_name == "ask_question":
                    last_question = state["questions"][-1]
                    print(f"Sending question: {last_question}")
                    await websocket.send_json({"type":"question",
                                            "payload": last_question})
                    data = await websocket.receive_json()
                    messgae_type= data.get("type")
                    payload = data.get("payload")
                    print(payload)
                    if messgae_type == "answer":
                        state["responses"].append(payload)
                elif q_index == 6 and node_name == "summary_agent":
                    print(f"Sending summary: {state['summary']}")
                    await websocket.send_json({"type":"summary",
                                            "payload": state["summary"]})
                elif q_index == 7 and node_name == "ask_question":
                    last_question = state["questions"][-1]
                    await websocket.send_json({"type":"question",
                                            "payload": last_question})
                    data = await websocket.receive_json()
                    messgae_type= data.get("type")
                    payload = data.get("payload")
                    if messgae_type == "answer":
                        state["responses"].append(payload)
                elif "redo" in state["sum_recap_intent"].lower() and node_name == "ask_question":
                    last_question = state["questions"][-1]
                    await websocket.send_json({"type":"question",
                                            "payload": last_question})
                    data = await websocket.receive_json()
                    messgae_type= data.get("type")
                    payload = data.get("payload")
                    if messgae_type == "answer":
                        #state = human_node(state, payload)
                        state["responses"].append(payload)
                elif q_index == 8 and node_name == "ask_question":
                    last_question = state["questions"][-1]
                    await websocket.send_json({"type":"question",
                                            "payload": last_question})
                    data = await websocket.receive_json()
                    messgae_type= data.get("type")
                    payload = data.get("payload")
                    if messgae_type == "answer":
                        state["responses"].append(payload)
                elif node_name == "brand_story_map":
                    #if state["url"]=="":
                    # DEBUG: Add breakpoint before setting URL in state
                    #import pdb; pdb.set_trace()  # Breakpoint 4: Before setting URL in state
                    #print(f"Before setting state['url'] = {url}")
                    #state["url"] = url
                    #print(f"After setting state['url'] = {state['url']}")
                    #     url_msg= "Give the url of website home page for which analysis will be performed"
                    #     await websocket.send_json({"type":"request_url",
                    #                                 "payload":url_msg})
                    #     data = await websocket.receive_json()
                    #     messgae_type= data.get("type")
                    #     payload = data.get("payload")
                    #     if messgae_type == "send_url" and payload and payload.strip(): # Check type and non-empty payload
                    #         print(f"Received URL: {payload}")
                    #         state["url"] = payload.strip()
                    #         print(f"Url in state: {state['url']}")
                    if state["bs_map"]:
                        await websocket.send_json({"type":"bs_map" ,
                                            "payload": state["bs_map"]})


                elif state["sections"] and node_name == "home_page":
                    await websocket.send_json({"type":"home_page_analysis",
                                                "payload":state["sections"]})
                elif state["themes"] and node_name == "wordpress_theme":
                    await websocket.send_json({"type":"wp_themes",
                                                "payload":state["themes"]})

                elif state["updated_page_content"] and node_name == "text_content":
                    await websocket.send_json({"type":"text_content",
                                                "payload":state["updated_page_content"]})
                elif node_name == "image_generation":
                    await websocket.send_json({"type":"completed",
                                                "payload":state})
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")