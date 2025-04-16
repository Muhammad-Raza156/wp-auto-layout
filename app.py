import streamlit as st
import json
import websockets
import asyncio
import time
import threading
import queue

# Configure page settings
st.set_page_config(
    page_title="Content Creation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a message queue for thread communication
if "message_queue" not in st.session_state:
    st.session_state.message_queue = queue.Queue()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = False
if "url" not in st.session_state:
    st.session_state.url = ""
if "summary" not in st.session_state:
    st.session_state.summary = None
if "bs_map" not in st.session_state:
    st.session_state.bs_map = None
if "home_page_analysis" not in st.session_state:
    st.session_state.home_page_analysis = None
if "wp_themes" not in st.session_state:
    st.session_state.wp_themes = None
if "text_content" not in st.session_state:
    st.session_state.text_content = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "completed" not in st.session_state:
    st.session_state.completed = False
if "ws_thread" not in st.session_state:
    st.session_state.ws_thread = None
if "should_disconnect" not in st.session_state:
    st.session_state.should_disconnect = False
if "outgoing_queue" not in st.session_state:
    st.session_state.outgoing_queue = queue.Queue()

# Process any messages in the queue
def process_messages_from_queue():
    while not st.session_state.message_queue.empty():
        try:
            message = st.session_state.message_queue.get_nowait()
            message_type = message.get("type")
            payload = message.get("payload")

            if message_type == "question":
                st.session_state.current_question = payload
                st.session_state.messages.append({"role": "assistant", "content": payload})

            elif message_type == "summary":
                st.session_state.summary = payload
                st.session_state.messages.append({"role": "assistant", "content": "I've prepared a summary based on our conversation."})

            elif message_type == "bs_map":
                st.session_state.bs_map = payload
                st.session_state.messages.append({"role": "assistant", "content": "I've created a brand story map for you."})

            elif message_type == "request_url":
                st.session_state.messages.append({"role": "assistant", "content": payload})

            elif message_type == "home_page_analysis":
                st.session_state.home_page_analysis = payload
                st.session_state.messages.append({"role": "assistant", "content": "Homepage analysis is complete."})

            elif message_type == "wp_themes":
                st.session_state.wp_themes = payload
                st.session_state.messages.append({"role": "assistant", "content": "WordPress theme suggestions are ready."})

            elif message_type == "text_content":
                st.session_state.text_content = payload
                st.session_state.messages.append({"role": "assistant", "content": "Updated page content is ready."})

            elif message_type == "completed":
                st.session_state.completed = True
                st.session_state.messages.append({"role": "assistant", "content": "Workflow completed! You can review all generated content in the tabs above."})

            elif message_type == "connection_status":
                st.session_state.connected = payload
        except queue.Empty:
            break

# WebSocket thread function
def websocket_thread(url, message_queue, outgoing_queue):
    async def connect_and_listen():
        try:
            websocket = await websockets.connect(url)
            message_queue.put({"type": "connection_status", "payload": True})

            # Start a task to process outgoing messages
            async def process_outgoing():
                while True:
                    try:
                        if outgoing_queue.empty():
                            await asyncio.sleep(0.1)
                            continue

                        message = outgoing_queue.get_nowait()
                        await websocket.send(json.dumps(message))
                    except Exception as e:
                        print(f"Error sending message: {e}")
                        await asyncio.sleep(0.1)

            # Start the outgoing message task
            asyncio.create_task(process_outgoing())

            # Listen for incoming messages
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    message_queue.put(data)
                except websockets.exceptions.ConnectionClosed:
                    message_queue.put({"type": "connection_status", "payload": False})
                    break
                except Exception as e:
                    print(f"WebSocket error: {e}")
                    break

        except Exception as e:
            print(f"Failed to connect: {e}")
            message_queue.put({"type": "connection_status", "payload": False})

    # Create and run the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(connect_and_listen())

# UI Components
st.title("Content Creation Workflow")

# Process any pending messages
process_messages_from_queue()

# Sidebar for connection and status
with st.sidebar:
    st.header("Connection")
    websocket_url = st.text_input("WebSocket URL", value="ws://localhost:8000/ws")

    col1, col2 = st.columns(2)
    with col1:
        connect_button = st.button("Connect", use_container_width=True)
    with col2:
        disconnect_button = st.button("Disconnect", use_container_width=True)

    st.divider()
    st.subheader("Status")
    connection_status = st.empty()
    if st.session_state.connected:
        connection_status.success("Connected")
    else:
        connection_status.error("Disconnected")

# Handle connection button
if connect_button and not st.session_state.connected:
    # Check if thread is already running
    if "ws_thread" in st.session_state and st.session_state.ws_thread and st.session_state.ws_thread.is_alive():
        st.warning("Connection already in progress...")
    else:
        # --- START: Reset Session State ---
        st.session_state.messages = []
        st.session_state.url = ""
        st.session_state.summary = None
        st.session_state.bs_map = None
        st.session_state.home_page_analysis = None
        st.session_state.wp_themes = None
        st.session_state.text_content = None
        st.session_state.current_question = None
        st.session_state.completed = False
        st.session_state.should_disconnect = False # Reset disconnect flag

        # Clear queues to avoid processing old messages/commands (Important!)
        while not st.session_state.message_queue.empty():
            try:
                st.session_state.message_queue.get_nowait()
            except queue.Empty:
                break
        while not st.session_state.outgoing_queue.empty():
            try:
                st.session_state.outgoing_queue.get_nowait()
            except queue.Empty:
                break
        # --- END: Reset Session State ---

        st.info("Attempting to connect...")
        # Start the WebSocket thread
        thread = threading.Thread(
            target=websocket_thread,
            args=(websocket_url, st.session_state.message_queue, st.session_state.outgoing_queue),
            daemon=True
        )
        thread.start()
        st.session_state.ws_thread = thread
        time.sleep(1)  # Give time for connection to establish
        st.rerun()

# Handle disconnect button
if disconnect_button and st.session_state.connected:
    # Send a disconnect message via the outgoing queue
    st.session_state.should_disconnect = True
    st.session_state.connected = False
    # The thread will terminate naturally when the WebSocket is closed
    st.rerun()

# Main content area - split into tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Conversation", "Summary", "Brand Story Map", "Website Analysis", "Generated Content"])

# Conversation tab
with tab1:
    st.subheader("Conversation")

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input area for user responses
    if st.session_state.connected and st.session_state.current_question:
        user_input = st.chat_input("Type your response here...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Send via the outgoing queue
            st.session_state.outgoing_queue.put({"type": "answer", "payload": user_input})
            st.session_state.current_question = None
            st.rerun()

    # URL input handling
    # if st.session_state.connected and any("Give the url of website" in msg.get("content", "") for msg in st.session_state.messages if msg["role"] == "assistant"):
    #     if not st.session_state.url:
    #         url_input = st.text_input("Enter website URL:")
    #         submit_url = st.button("Submit URL")
    #         if submit_url and url_input:
    #             # DEBUG: Add breakpoint here to track URL input
    #             import pdb; pdb.set_trace()  # Breakpoint 1: URL input from UI
    #             st.session_state.url = url_input
    #             st.session_state.messages.append({"role": "user", "content": url_input})
    #             # Send via the outgoing queue
    #             st.session_state.outgoing_queue.put({"type": "send_url", "payload": url_input})
    #             # DEBUG: Add another breakpoint after sending URL
    #             import pdb; pdb.set_trace()  # Breakpoint 2: After sending URL
    #             st.rerun()

# Summary tab
with tab2:
    st.subheader("Content Summary")
    if st.session_state.summary:
        st.markdown(st.session_state.summary)
    else:
        st.info("Summary will appear here once generated.")

# Brand Story Map tab
with tab3:
    st.subheader("Brand Story Map")
    if st.session_state.bs_map:
        st.markdown(st.session_state.bs_map)
    else:
        st.info("Brand story map will appear here once generated.")

# Website Analysis tab
with tab4:
    st.subheader("Website Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Homepage Analysis")
        if st.session_state.home_page_analysis:
            st.markdown(st.session_state.home_page_analysis)
        else:
            st.info("Homepage analysis will appear here once generated.")

    with col2:
        st.markdown("### WordPress Theme Suggestions")
        if st.session_state.wp_themes:
            # Check if wp_themes is a dictionary
            if isinstance(st.session_state.wp_themes, dict):
                for theme_name, theme_details in st.session_state.wp_themes.items():
                    with st.expander(theme_name):
                        st.markdown(theme_details)
            else:
                st.markdown(st.session_state.wp_themes)
        else:
            st.info("WordPress theme suggestions will appear here once generated.")

# Generated Content tab
with tab5:
    st.subheader("Updated Page Content")
    if st.session_state.text_content:
        st.markdown(st.session_state.text_content)
    else:
        st.info("Updated page content will appear here once generated.")

# Add a periodic rerun to update the UI with new messages from the queue
if st.session_state.connected:
    time.sleep(0.5)  # Short delay to trigger periodic reruns
    st.rerun()