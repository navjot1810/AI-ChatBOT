import os
import json
import uuid
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from dotenv import load_dotenv
from streamlit_mic_recorder import speech_to_text

# =========================================================
# CONFIGURATION
# =========================================================
load_dotenv()
st.set_page_config(
    page_title="AI ChatBOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("GEMINI_API_KEY")
# Set GEMINI_MODEL in .env to a model available to your API key.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
HISTORY_FILE = "chat_history.json"

if API_KEY:
    genai.configure(api_key=API_KEY)

# =========================================================
# CHAT HISTORY
# =========================================================
def load_chats():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_chats():
    temp_path = HISTORY_FILE + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chats, f, ensure_ascii=False, indent=2)
    os.replace(temp_path, HISTORY_FILE)


def create_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "created": datetime.now().isoformat(timespec="seconds"),
        "messages": [],
    }
    st.session_state.active_chat_id = chat_id
    # Called from a button callback / before the input widget is rendered.
    st.session_state.chat_input = ""
    st.session_state.pending_prompt = None
    save_chats()


def submit_message():
    """Widget callback: capture text and clear it before the next render."""
    prompt = st.session_state.get("chat_input", "").strip()
    if prompt:
        st.session_state.pending_prompt = prompt
        # Safe here because on_change/on_click callbacks run before widgets render.
        st.session_state.chat_input = ""


def switch_chat(chat_id):
    st.session_state.active_chat_id = chat_id
    st.session_state.chat_input = ""
    st.session_state.pending_prompt = None


def clear_current_chat():
    active = st.session_state.active_chat_id
    if active in st.session_state.chats:
        st.session_state.chats[active]["messages"] = []
        st.session_state.chats[active]["title"] = "New Chat"
    st.session_state.chat_input = ""
    st.session_state.pending_prompt = None
    save_chats()


if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if st.session_state.active_chat_id not in st.session_state.chats:
    st.session_state.active_chat_id = next(iter(st.session_state.chats), None)
if "think_mode" not in st.session_state:
    st.session_state.think_mode = False
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if not st.session_state.chats:
    create_chat()

# =========================================================
# GEMINI RESPONSE
# =========================================================
def get_response(messages, prompt, think_mode=False):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from your .env file.")

    instruction = (
        "You are a helpful, accurate, friendly AI assistant. "
        "Use clear language, headings, and examples when useful."
    )
    if think_mode:
        instruction += (
            " Be especially careful with complex questions, check assumptions, "
            "verify calculations where possible, and provide a structured, detailed answer. "
            "Briefly explain your approach without revealing private hidden chain-of-thought."
        )

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=instruction,
    )
    history = []
    for item in messages:
        role = item.get("role")
        content = item.get("content", "")
        if role == "user":
            history.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            history.append({"role": "model", "parts": [content]})
    chat = model.start_chat(history=history)
    response = chat.send_message(prompt)
    return response.text or "Gemini returned an empty response."

# =========================================================
# READ ALOUD
# =========================================================
def speaker_button(text, key):
    safe_text = json.dumps(text, ensure_ascii=False)
    safe_key = "".join(c for c in key if c.isalnum() or c == "_")
    components.html(
        f"""
        <button id="speak_{safe_key}" style="background:#202b45;color:#e8edff;"
        "border:1px solid #435174;border-radius:10px;padding:7px 12px;"
        "cursor:pointer;font-size:14px;">🔊 Read aloud</button>
        <script>
        const btn = document.getElementById("speak_{safe_key}");
        const speechText = {safe_text};
        btn.onclick = () => {{
          if (!window.speechSynthesis) {{ alert("Speech output is not supported."); return; }}
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(speechText);
          utterance.lang = "en-IN";
          utterance.rate = 1;
          window.speechSynthesis.speak(utterance);
        }};
        </script>
        """,
        height=48,
    )

# =========================================================
# STYLING
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
      background: radial-gradient(ellipse at 50% -20%, rgba(86,108,255,.22), transparent 55%), #0b1020;
      color: #eef2ff;
    }
    .main .block-container {
      max-width: 900px;
      padding: 2rem 1.3rem 150px;
    }
    h1,h2,h3 { color:#f8faff !important; }
    [data-testid="stMarkdownContainer"] p { color:#c4cce0; }
    [data-testid="stChatMessage"] {
      background:rgba(25,34,57,.78); border:1px solid rgba(160,177,220,.15);
      border-radius:18px; padding:1rem; margin:.8rem 0;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background:rgba(67,82,148,.28); }
    section[data-testid="stSidebar"] { background:#0e1528; border-right:1px solid #293450; }
    div.stButton > button { border-radius:12px; min-height:42px; }
    div[data-testid="stTextInput"] input {
      min-height:42px; border:1px solid rgba(151,169,216,.35); border-radius:12px;
      background:#131b2e; color:#fff;
    }
    div[data-testid="stCheckbox"] { padding-top:6px; }
    div[data-testid="stHorizontalBlock"] { align-items:center; gap:.35rem; }
    /* Pin the complete input row to the bottom of the chat viewport. */
    .st-key-input_bar {
      position:fixed;
      bottom:12px;
      z-index:9999;
      width:min(900px, calc(100vw - 340px));
      left:calc(50% + 160px);
      transform:translateX(-50%);
      box-sizing:border-box;
      background:rgba(11,16,32,.97);
      border:1px solid #34415f;
      border-radius:16px;
      padding:.6rem .75rem;
      box-shadow:0 -8px 28px rgba(0,0,0,.25);
      backdrop-filter:blur(12px);
    }
    .st-key-input_bar [data-testid="stTextInput"] input { background:transparent; border:none; box-shadow:none; }
    .st-key-input_bar [data-testid="stCheckbox"] { padding-top:0; white-space:nowrap; }
    @media (max-width:1100px) {
      .st-key-input_bar {
        left:50%;
        width:calc(100vw - 2rem);
      }
    }
    @media (max-width:700px) {
      section[data-testid="stSidebar"] { min-width:0; }
      .main .block-container { padding:1.2rem .7rem 150px; }
      .st-key-input_bar {
        left:50%;
        bottom:6px;
        width:calc(100vw - 1rem);
        padding:.4rem;
      }
      .st-key-input_bar [data-testid="stCheckbox"] label p { font-size:11px; }
      .st-key-input_bar [data-testid="stHorizontalBlock"] { gap:.2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🤖 AI ChatBOT")
    st.caption("Your personal Gemini assistant")

    st.button("＋ New chat", use_container_width=True, on_click=create_chat)
    st.divider()
    st.markdown("### 🕘 Chat history")

    sorted_chats = sorted(
        st.session_state.chats.items(),
        key=lambda pair: pair[1].get("created", ""),
        reverse=True,
    )
    for chat_id, chat_data in sorted_chats:
        title = chat_data.get("title", "New Chat")
        active = chat_id == st.session_state.active_chat_id
        left, right = st.columns([5, 1])
        with left:
            st.button(
                ("▸ " if active else "") + title[:30],
                key=f"open_chat_{chat_id}",
                use_container_width=True,
                on_click=switch_chat,
                args=(chat_id,),
            )
        with right:
            if st.button("✕", key=f"delete_chat_{chat_id}", help="Delete this chat"):
                del st.session_state.chats[chat_id]
                if st.session_state.active_chat_id == chat_id:
                    st.session_state.active_chat_id = next(iter(st.session_state.chats), None)
                if not st.session_state.chats:
                    create_chat()
                save_chats()
                st.rerun()

    st.divider()
    st.markdown("### ⚙️ Chat settings")
    st.caption(f"Model: {MODEL_NAME}")
    st.caption("Provider: Google Gemini")
    st.button("🗑️ Clear current chat", use_container_width=True, on_click=clear_current_chat)
    st.caption("Chat history is saved locally in chat_history.json.")

# =========================================================
# MAIN CHAT WINDOW
# =========================================================
active_id = st.session_state.active_chat_id
current_chat = st.session_state.chats[active_id]
st.title("🤖 AI ChatBOT")
st.markdown("<p style='text-align:center'>Ask anything. Powered by Gemini.</p>", unsafe_allow_html=True)

for index, message in enumerate(current_chat["messages"]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            speaker_button(message["content"], f"{active_id.replace('-', '')}_{index}")

# =========================================================
# FIXED INPUT BAR: MESSAGE + THINK + VOICE + SEND
# =========================================================
with st.container(key="input_bar", border=True):
    input_cols = st.columns([7.0, 1.4, 1.0, 1.0], gap="small")

    # Render voice widget before text input, so a transcript can populate it safely.
    # If microphone access fails, users can still type and send messages normally.
    with input_cols[2]:
        try:
            recognized_text = speech_to_text(
                language="en-IN",
                start_prompt="🎙️",
                stop_prompt="⏹️",
                just_once=True,
                key=f"voice_recognition_{active_id}",
            )
        except Exception as mic_exc:
            recognized_text = None
            st.caption("🎙️ Mic unavailable. Allow microphone access in your browser and check that streamlit-mic-recorder is installed.")

    if recognized_text and recognized_text.strip():
        # Only write a new transcript once, avoiding overwriting text on every rerun.
        transcript = recognized_text.strip()
        if transcript != st.session_state.get("last_voice_transcript"):
            st.session_state.last_voice_transcript = transcript
            st.session_state.chat_input = transcript

    with input_cols[0]:
        st.text_input(
            "Message",
            placeholder="Ask anything...",
            key="chat_input",
            label_visibility="collapsed",
            on_change=submit_message,
        )
    with input_cols[1]:
        st.checkbox("🧠 Think", key="think_mode", help="Give more detailed answers")
    with input_cols[3]:
        st.button(
            "➤",
            key=f"send_message_{active_id}",
            help="Send message",
            use_container_width=True,
            type="primary",
            on_click=submit_message,
        )

# Process queued prompt after input callbacks. Do NOT assign chat_input here:
# changing a widget's state after rendering it causes StreamlitWidgetAlreadyInstantiatedError.
prompt = st.session_state.pending_prompt
if prompt:
    st.session_state.pending_prompt = None
    current_chat["messages"].append({"role": "user", "content": prompt})
    if current_chat["title"] == "New Chat":
        current_chat["title"] = prompt[:35] + ("..." if len(prompt) > 35 else "")
    save_chats()

    # Render the submitted user message in this run, before waiting for Gemini.
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking carefully..." if st.session_state.think_mode else "✨ Gemini is answering..."):
                answer = get_response(
                    current_chat["messages"][:-1],
                    prompt,
                    think_mode=st.session_state.think_mode,
                )
                st.markdown(answer)
                speaker_button(answer, f"new_{uuid.uuid4().hex[:12]}")
        current_chat["messages"].append({"role": "assistant", "content": answer})
        save_chats()
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        error_text = str(exc)
        if "404" in error_text or "NOT_FOUND" in error_text:
            st.error(
                f"Model '{MODEL_NAME}' is unavailable for this API key. "
                "Set GEMINI_MODEL in .env to a model supported by your Google AI Studio account."
            )
        elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            st.error("Gemini API quota exceeded. Check your Google AI Studio quota.")
        elif "API_KEY_INVALID" in error_text or "API key not valid" in error_text:
            st.error("Invalid Gemini API key. Check your .env file.")
        else:
            st.error(f"Gemini error: {error_text}")
    st.rerun()
