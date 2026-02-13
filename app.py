import streamlit as st
import google.generativeai as genai

# ---------- CONFIG ----------
st.set_page_config(page_title="Pixel AI Companion", page_icon="💖")

# ---------- GEMINI SETUP ----------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except FileNotFoundError:
    st.error("⚠️ Secret key not found! Please create a `.streamlit/secrets.toml` file.")
    st.stop()
except KeyError:
    st.error("⚠️ Key `GEMINI_API_KEY` not found in secrets.toml.")
    st.stop()

# --- GEMINI CONFIGURATION ---
try:
    genai.configure(api_key=api_key)
    # We lower the 'temperature' to 0.5 to make the bot less creative and more rule-following
    generation_config = genai.types.GenerationConfig(temperature=0.5)
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config
    )
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background: url("bgg.gif") no-repeat center center fixed;
    background-size: cover;
    font-family: 'VT323', monospace;
    color: white;
}

body::before {
    content:"";
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.55);
    z-index:-1;
}

/* USER BUBBLE */
.chat-bubble-user {
    background: #ff4fa3;
    border: 2px solid #ff2e92;
    padding: 14px 22px;
    border-radius: 30px;
    margin: 12px 0;
    text-align: right;
    color: white;
    font-size: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}

/* BOT BUBBLE */
.chat-bubble-bot {
    background: rgba(0,0,0,0.6);
    border: 2px solid #ff4fa3;
    padding: 14px 22px;
    border-radius: 30px;
    margin: 12px 0;
    text-align: left;
    color: white;
    font-size: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}
</style>

""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    "<h2 style='text-align:center; color:#ff4fa3;'>PIXEL AI COMPANION 💗</h2>",
    unsafe_allow_html=True
)

# ---------- SESSION MEMORY ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- DISPLAY CHAT ----------
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'>{message['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble-bot'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# ---------- INPUT ----------
user_input = st.text_input("Ask your pixel companion...")

if st.button("Send"):
    if user_input:
        # Save user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        # Generate AI response
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            bot_reply = response.text

        # Save bot reply
        st.session_state.chat_history.append(
            {"role": "bot", "content": bot_reply}
        )

        st.rerun()
