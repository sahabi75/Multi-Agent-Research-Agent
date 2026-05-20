import streamlit as st
import requests
import json
import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title = "Research Assistant",
    page_icon  = "🔍",
    layout     = "wide"
)

BACKEND_URL = "http://localhost:8000"
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHATS_FILE = "frontend/saved_chats.json"


def load_all_chats():
    if not os.path.exists(CHATS_FILE):
        return []
    with open(CHATS_FILE, "r") as f:
        return json.load(f)


def save_all_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=2)


def save_current_chat():
    if not st.session_state.chat_history:
        return

    chats = load_all_chats()

    # Use first user message as title
    title = "New Chat"
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            title = msg["content"][:50]   # first 50 chars
            break

    # Check if this chat already exists — update it
    for chat in chats:
        if chat["id"] == st.session_state.current_chat_id:
            chat["title"]    = title
            chat["messages"] = st.session_state.chat_history
            chat["date"]     = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_all_chats(chats)
            return

    # New chat — add it
    new_chat = {
        "id"      : st.session_state.current_chat_id,
        "title"   : title,
        "messages": st.session_state.chat_history,
        "date"    : datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    chats.append(new_chat)
    save_all_chats(chats)


def start_new_chat():
    # Save current chat before starting new one
    save_current_chat()
    # Reset session for new chat
    st.session_state.chat_history    = []
    st.session_state.last_report     = ""
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    st.rerun()


def load_chat(chat_id):
    # Save current chat first
    save_current_chat()
    # Load selected chat
    chats = load_all_chats()
    for chat in chats:
        if chat["id"] == chat_id:
            st.session_state.chat_history    = chat["messages"]
            st.session_state.current_chat_id = chat_id
            # Find last report in messages
            st.session_state.last_report = ""
            for msg in reversed(chat["messages"]):
                if msg["role"] == "assistant" and msg.get("is_report"):
                    st.session_state.last_report = msg["content"]
                    break
            st.rerun()


def delete_chat(chat_id):
    chats     = load_all_chats()
    new_chats = [c for c in chats if c["id"] != chat_id]
    save_all_chats(new_chats)
    # If deleted current chat → start new
    if chat_id == st.session_state.current_chat_id:
        start_new_chat()
    else:
        st.rerun()


# Session state setup

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_report" not in st.session_state:
    st.session_state.last_report = ""

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")



# Helper functions

def is_research_question(message, chat_history):
    history_text = ""
    for msg in chat_history[-4:]:
        role    = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:200]
        history_text += f"{role}: {content}\n"

    prompt = f"""
You are a classifier. Decide if the user's message is:
- A NEW research question that needs web research (answer: YES)
- A follow up, chat, summary request, or casual message (answer: NO)

Recent conversation:
{history_text}

User's new message: "{message}"

Reply with only YES or NO. Nothing else.
"""
    response = groq_client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",
        messages = [{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content.strip().upper()
    return "YES" in answer


def answer_followup(user_message, chat_history, last_report):
    messages = []
    system   = "You are a helpful research assistant. Answer based on the conversation and last research report."
    if last_report:
        system += f"\n\nLast research report:\n{last_report[:2000]}"
    messages.append({"role": "system", "content": system})
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"][:500]})
    messages.append({"role": "user", "content": user_message})
    response = groq_client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",
        messages = messages
    )
    return response.choices[0].message.content.strip()


def run_research(question):
    try:
        response = requests.post(
            f"{BACKEND_URL}/research",
            json    = {"questions": [question]},
            timeout = 120
        )
        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                return results[0]["report"]
        return "❌ No report generated."
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure FastAPI server is running!"
    except Exception as e:
        return f"❌ Error: {str(e)}"



# SIDEBAR  New Chat + Saved Chats

with st.sidebar:

    st.title("💬 My Chats")

    # New Chat button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        start_new_chat()

    st.divider()

    # Load and show all saved chats
    all_chats = load_all_chats()

    if not all_chats:
        st.write("No saved chats yet.")
        st.write("Start asking questions!")

    else:
        st.write(f"**{len(all_chats)} saved chat(s)**")
        st.write("")

        # Show newest chats first
        for chat in reversed(all_chats):

            # Highlight current chat
            is_current = chat["id"] == st.session_state.current_chat_id

            
            label = f"{'📌 ' if is_current else '💬 '}{chat['title']}"

            col1, col2 = st.columns([5, 1])

            with col1:
                if st.button(label, key=f"load_{chat['id']}", use_container_width=True):
                    load_chat(chat["id"])

            with col2:
                
                if st.button("🗑", key=f"del_{chat['id']}"):
                    delete_chat(chat["id"])

            # Show date under each chat
            st.caption(chat["date"])



# MAIN AREA — Chat Window

st.title("🔍 Research Assistant")
st.write("Ask me anything! I will research it and give you a full report.")
st.divider()

# Show welcome message if no chat yet
if not st.session_state.chat_history:
    st.info("👋 Start by typing a research question below!")

# Show all messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("is_report"):
            st.download_button(
                label    = "⬇️ Download Report",
                data     = message["content"],
                file_name= "report.md",
                mime     = "text/markdown",
                key      = message["key"]
            )

# Chat input
user_input = st.chat_input("Ask a research question or chat...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({
        "role"     : "user",
        "content"  : user_input,
        "is_report": False,
        "key"      : ""
    })

    with st.chat_message("assistant"):
        needs_research = is_research_question(
            user_input,
            st.session_state.chat_history
        )

        if needs_research:
            with st.spinner("🤖 Researching... please wait (30-60 seconds)"):
                reply = run_research(user_input)
            st.session_state.last_report = reply
            is_report = True
            st.markdown(reply)
            key = f"dl_{len(st.session_state.chat_history)}"
            st.download_button(
                label    = "⬇️ Download Report",
                data     = reply,
                file_name= "report.md",
                mime     = "text/markdown",
                key      = key
            )
        else:
            with st.spinner("💬 Thinking..."):
                reply = answer_followup(
                    user_input,
                    st.session_state.chat_history,
                    st.session_state.last_report
                )
            is_report = False
            key       = f"msg_{len(st.session_state.chat_history)}"
            st.markdown(reply)

    st.session_state.chat_history.append({
        "role"     : "assistant",
        "content"  : reply,
        "is_report": is_report,
        "key"      : key
    })

    
    save_current_chat()
    st.rerun()