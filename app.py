import streamlit as st
import google.generativeai as genai

# ---------- CONFIG ----------
st.set_page_config(page_title="CHATBOT", page_icon="")

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

/* IMPORT PIXEL FONTS */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

/* BACKGROUND */
body {
    font-family:'VT323', monospace;
    background: url("bgg.gif") no-repeat center center fixed;
    background-size: cover;
    min-height:100vh;
    color:white;
}

/* DARK OVERLAY */
body::before{
    content:"";
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.55);
    z-index:-1;
}

/* CHAT CONTAINER (LIKE TASK CARDS STYLE) */
.chat-container{
    width:80%;
    max-width:800px;
    margin:50px auto;
    padding:30px;
    border-radius:30px;
    background:rgba(0,0,0,0.6);
    border:2px solid #ff4fa3;
    box-shadow:0 8px 20px rgba(0,0,0,0.5);
}

/* TITLE (PIXEL STYLE) */
.chat-title{
    font-family:'Press Start 2P';
    font-size:14px;
    text-align:center;
    margin-bottom:30px;
    color:#ff4fa3;
}

/* USER BUBBLE */
.chat-bubble-user{
    background:#ff4fa3;
    border:2px solid #ff2e92;
    padding:16px 24px;
    border-radius:30px;
    margin:15px 0;
    text-align:right;
    font-size:22px;
    box-shadow:0 6px 15px rgba(0,0,0,0.4);
}

/* BOT BUBBLE */
.chat-bubble-bot{
    background:rgba(0,0,0,0.7);
    border:2px solid #ff4fa3;
    padding:16px 24px;
    border-radius:30px;
    margin:15px 0;
    text-align:left;
    font-size:22px;
    box-shadow:0 6px 15px rgba(0,0,0,0.4);
}

/* OPTIONAL INPUT AREA (MATCHES TASK INPUT STYLE) */
.chat-input{
    display:flex;
    margin-top:25px;
    gap:10px;
}

.chat-input input{
    flex:1;
    padding:15px 20px;
    border-radius:40px;
    border:2px solid #ff2e92;
    background:#ff4fa3;
    color:white;
    font-size:20px;
    font-family:'VT323';
    outline:none;
}

.chat-input button{
    padding:12px 20px;
    border-radius:30px;
    border:none;
    background:#ff2e92;
    color:white;
    font-family:'VT323';
    font-size:20px;
    cursor:pointer;
}

.chat-input button:hover{
    opacity:0.85;
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
