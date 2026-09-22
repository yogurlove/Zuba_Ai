import streamlit as st
import requests
import os
import html
import base64

st.set_page_config(
    page_title="Chill Bro AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MODEL = "gpt-5.6-luna"

LANGUAGES = [
    "English", "Hindi", "Punjabi", "Nepali", "Urdu", "Bengali",
    "Tamil", "Telugu", "Marathi", "Gujarati", "Kannada", "Malayalam",
    "Odia", "Assamese", "Maithili", "Sanskrit", "Kashmiri", "Sindhi",
    "Konkani", "Dogri", "Manipuri", "Bodo", "Santali",
    "French", "Spanish", "German", "Italian", "Portuguese", "Russian",
    "Ukrainian", "Polish", "Dutch", "Swedish", "Norwegian", "Danish",
    "Finnish", "Icelandic", "Irish", "Welsh", "Greek", "Romanian",
    "Hungarian", "Czech", "Slovak", "Bulgarian", "Serbian", "Croatian",
    "Bosnian", "Slovenian", "Albanian", "Macedonian", "Lithuanian",
    "Latvian", "Estonian", "Maltese", "Catalan", "Basque", "Galician",
    "Luxembourgish", "Frisian", "Occitan", "Corsican",
    "Arabic", "Hebrew", "Persian", "Turkish", "Kurdish", "Armenian",
    "Georgian", "Azerbaijani", "Kazakh", "Uzbek", "Turkmen", "Kyrgyz",
    "Tajik", "Mongolian", "Pashto", "Dari",
    "Chinese", "Japanese", "Korean", "Vietnamese", "Thai", "Indonesian",
    "Malay", "Filipino", "Burmese", "Khmer", "Lao", "Sinhala",
    "Javanese", "Sundanese",
    "Swahili", "Amharic", "Somali", "Hausa", "Yoruba", "Igbo", "Zulu",
    "Xhosa", "Afrikaans", "Sesotho", "Setswana", "Shona", "Kinyarwanda",
    "Malagasy", "Samoan", "Tongan", "Fijian", "Maori", "Hawaiian",
    "Haitian Creole", "Esperanto", "Latin",
]

PERSONALITIES = {
    "😎 Chill Bro": "Relaxed, friendly, casual and naturally funny.",
    "😂 Funny": "Playful, humorous and entertaining.",
    "🧠 Smart": "Precise, intelligent, logical and educational.",
    "❤️ Lovely": "Warm, kind, positive and supportive.",
    "🤝 Best Friend": "Talk naturally like a close best friend. Casual, honest and supportive.",
    "💀 Extreme Toxic": (
        "Use playful fictional bro-style trash talk with strong profanity "
        "such as fuck, shit, damn and dumbass when appropriate. "
        "Keep it playful and non-threatening. "
        "Never use hateful slurs, threats, violence or attacks on protected groups."
    ),
}

STUDY_TOOLS = [
    "📖 Explain Topic",
    "📝 Summarize Notes",
    "❓ Generate Quiz",
    "🧠 Flashcards",
    "✍️ Homework Helper",
    "📅 Study Plan",
    "🔍 Exam Preparation",
]

GAMING_TOOLS = [
    "🎯 Game Tips",
    "🧠 Strategy Helper",
    "🔫 Builds / Loadouts",
    "⚔️ Weapon Comparison",
    "🗺️ Map / Mission Help",
    "🏆 Rank Improvement",
    "🎮 Settings / Sensitivity",
    "👾 Boss Fight Help",
    "🧩 Quest / Puzzle Help",
    "🛡️ Character / Team Build",
    "💻 PC / Mobile Optimization",
    "🎲 Game Recommendation",
]

THEMES = {
    "🌌 Neon Night": {
        "bg": "#070b18",
        "surface": "#0f172a",
        "card": "#111c33",
        "primary": "#22d3ee",
        "secondary": "#a855f7",
        "text": "#f8fafc",
        "muted": "#94a3b8",
        "input": "#0b1222",
    },
    "💜 Purple": {
        "bg": "#0b0714",
        "surface": "#171025",
        "card": "#1d1430",
        "primary": "#c084fc",
        "secondary": "#8b5cf6",
        "text": "#faf5ff",
        "muted": "#c4b5fd",
        "input": "#120b20",
    },
    "🌊 Ocean": {
        "bg": "#061218",
        "surface": "#0b2029",
        "card": "#102c38",
        "primary": "#22d3ee",
        "secondary": "#3b82f6",
        "text": "#f0fdfa",
        "muted": "#94a3b8",
        "input": "#081a22",
    },
    "💚 Matrix": {
        "bg": "#050b07",
        "surface": "#0b1710",
        "card": "#0f2116",
        "primary": "#22c55e",
        "secondary": "#86efac",
        "text": "#f0fdf4",
        "muted": "#86a98f",
        "input": "#07130b",
    },
    "🔥 Fire": {
        "bg": "#120806",
        "surface": "#21100a",
        "card": "#2b150d",
        "primary": "#fb923c",
        "secondary": "#f43f5e",
        "text": "#fff7ed",
        "muted": "#fdba74",
        "input": "#180b07",
    },
    "🌅 Sunset": {
        "bg": "#120a12",
        "surface": "#211020",
        "card": "#2c1426",
        "primary": "#fb7185",
        "secondary": "#f97316",
        "text": "#fff1f2",
        "muted": "#fda4af",
        "input": "#180b14",
    },
    "🖤 Dark": {
        "bg": "#080808",
        "surface": "#121212",
        "card": "#181818",
        "primary": "#ffffff",
        "secondary": "#9ca3af",
        "text": "#ffffff",
        "muted": "#9ca3af",
        "input": "#101010",
    },
}

defaults = {
    "messages": [],
    "theme": "🌌 Neon Night",
    "language": "English",
    "personality": "😎 Chill Bro",
    "mode": "🤖 Chill Bro Chat",
    "music_on": False,
    "music_volume": 0.25,
    "study_tool": "📖 Explain Topic",
    "gaming_tool": "🎯 Game Tips",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

theme = THEMES[st.session_state.theme]

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

html, body, [class*="css"] {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Helvetica,
        Arial,
        sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 15% 10%,
            {theme["primary"]}10,
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 80%,
            {theme["secondary"]}0d,
            transparent 35%
        ),
        {theme["bg"]};
    color: {theme["text"]};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stSidebar"] {{
    background: {theme["surface"]};
    border-right: 1px solid {theme["primary"]}25;
}}

.block-container {{
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}}

.app-header {{
    text-align: center;
    padding: 25px 10px 20px;
}}

.app-logo {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 58px;
    height: 58px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        {theme["primary"]},
        {theme["secondary"]}
    );
    box-shadow: 0 8px 35px {theme["primary"]}30;
    font-size: 30px;
    margin-bottom: 14px;
}}

.app-title {{
    margin: 0;
    font-size: clamp(32px, 7vw, 48px);
    font-weight: 800;
    letter-spacing: -1.5px;
    color: {theme["text"]};
}}

.app-title span {{
    color: {theme["primary"]};
}}

.app-subtitle {{
    margin-top: 8px;
    color: {theme["muted"]};
    font-size: 15px;
}}

.mode-badge {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px;
    margin-top: 14px;
    border-radius: 999px;
    background: {theme["primary"]}12;
    border: 1px solid {theme["primary"]}30;
    color: {theme["primary"]};
    font-size: 13px;
    font-weight: 600;
}}

.welcome-card {{
    max-width: 700px;
    margin: 25px auto;
    padding: 28px;
    border-radius: 22px;
    background: {theme["card"]};
    border: 1px solid {theme["primary"]}18;
    box-shadow: 0 15px 45px rgba(0,0,0,.18);
    text-align: center;
}}

.welcome-icon {{
    font-size: 42px;
    margin-bottom: 10px;
}}

.welcome-title {{
    font-size: 21px;
    font-weight: 700;
    color: {theme["text"]};
}}

.welcome-text {{
    margin-top: 8px;
    color: {theme["muted"]};
    line-height: 1.6;
}}

.chat-row {{
    display: flex;
    width: 100%;
    margin: 6px 0;
}}

.chat-row.user {{
    justify-content: flex-end;
}}

.chat-row.ai {{
    justify-content: flex-start;
}}

.chat-bubble {{
    max-width: min(75%, 680px);
    padding: 10px 13px;
    border-radius: 14px;
    line-height: 1.5;
    font-size: 15px;
    overflow-wrap: anywhere;
    box-shadow: 0 1px 2px rgba(0,0,0,.18);
}}

.user-bubble {{
    background: #005c4b;
    color: #ffffff;
    border-bottom-right-radius: 4px;
}}

.ai-bubble {{
    background: #202c33;
    color: #e9edef;
    border-bottom-left-radius: 4px;
}}

[data-testid="stChatInput"] {{
    background: transparent !important;
}}

[data-testid="stChatInput"] > div {{
    background: {theme["input"]} !important;
    border: 1px solid {theme["primary"]}45 !important;
    border-radius: 18px !important;
}}

[data-testid="stChatInput"] textarea {{
    color: {theme["text"]} !important;
    -webkit-text-fill-color: {theme["text"]} !important;
    caret-color: {theme["primary"]} !important;
    background: transparent !important;
    font-size: 16px !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: {theme["muted"]} !important;
    -webkit-text-fill-color: {theme["muted"]} !important;
    opacity: 1 !important;
}}

.stButton > button {{
    border-radius: 12px !important;
    border: 1px solid {theme["primary"]}25 !important;
    background: {theme["card"]} !important;
    color: {theme["text"]} !important;
    font-weight: 600 !important;
}}

.stButton > button:hover {{
    border-color: {theme["primary"]}70 !important;
    color: {theme["primary"]} !important;
}}

div[data-baseweb="select"] > div {{
    background: {theme["card"]} !important;
    border-color: {theme["primary"]}20 !important;
}}

div[data-baseweb="select"] span {{
    color: {theme["text"]} !important;
}}

.footer {{
    text-align: center;
    color: {theme["muted"]};
    font-size: 12px;
    padding: 30px 0 10px;
}}

@media (max-width: 700px) {{

    .block-container {{
        padding: 1rem .75rem 6rem;
    }}

    .chat-bubble {{
        max-width: 85%;
        font-size: 15px;
    }}

    .app-title {{
        font-size: 34px;
    }}

}}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div style="
            font-size:22px;
            font-weight:800;
            color:{theme["text"]};
            padding-bottom:12px;
        ">
            🔥 <span style="color:{theme["primary"]};">
            Chill Bro
            </span> AI
        </div>
        """,
        unsafe_allow_html=True,
    )

    modes = [
        "🤖 Chill Bro Chat",
        "📚 Study Helper",
        "🎮 Gaming Helper",
    ]

    st.session_state.mode = st.radio(
        "Mode",
        modes,
        index=modes.index(st.session_state.mode),
    )

    st.divider()

    st.session_state.theme = st.selectbox(
        "🎨 Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(
            st.session_state.theme
        ),
    )

    st.session_state.language = st.selectbox(
        "🌍 Language",
        LANGUAGES,
        index=LANGUAGES.index(
            st.session_state.language
        ),
    )

    if st.session_state.mode == "🤖 Chill Bro Chat":

        st.session_state.personality = st.selectbox(
            "🎭 Personality",
            list(PERSONALITIES.keys()),
            index=list(PERSONALITIES.keys()).index(
                st.session_state.personality
            ),
        )

    elif st.session_state.mode == "📚 Study Helper":

        st.session_state.study_tool = st.selectbox(
            "📚 Study Tool",
            STUDY_TOOLS,
            index=STUDY_TOOLS.index(
                st.session_state.study_tool
            ),
        )

    else:

        st.session_state.gaming_tool = st.selectbox(
            "🎮 Gaming Tool",
            GAMING_TOOLS,
            index=GAMING_TOOLS.index(
                st.session_state.gaming_tool
            ),
        )

    st.divider()

    st.markdown("### 🎵 7 Week 3 Days")

    st.session_state.music_on = st.toggle(
        "🎵 Play Background Music",
        value=st.session_state.music_on,
    )

    st.session_state.music_volume = st.slider(
        "🔊 Music Volume",
        0.0,
        1.0,
        st.session_state.music_volume,
        0.05,
    )

    st.divider()

    if st.button(
        "🧹 Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# MUSIC
# ============================================================

def play_background_music():

    filename = "7 weeks & 3 days.mp3"

    if not os.path.exists(filename):

        st.warning(
            "🎵 `7week 3days.mp3` was not found. "
            "Put it in the same GitHub folder as `streamlit_app.py`."
        )

        return

    try:

        with open(filename, "rb") as audio_file:

            audio_data = base64.b64encode(
                audio_file.read()
            ).decode()

        volume = st.session_state.music_volume

        st.markdown(
            f"""
            <audio
                controls
                autoplay
                loop
                style="
                    width:100%;
                    height:38px;
                    margin:8px 0 15px 0;
                "
            >
                <source
                    src="data:audio/mpeg;base64,{audio_data}"
                    type="audio/mpeg"
                >
            </audio>

            <script>
            const audios = document.querySelectorAll("audio");

            audios.forEach(function(audio) {{
                audio.volume = {volume};
            }});
            </script>
            """,
            unsafe_allow_html=True,
        )

    except Exception:
        pass


if st.session_state.music_on:
    play_background_music()

# ============================================================
# HEADER
# ============================================================

if st.session_state.mode == "🤖 Chill Bro Chat":

    title = "Chill Bro <span>AI</span>"
    subtitle = "Your personal AI assistant, study partner and gaming bro."
    badge = "🤖 AI CHAT"

elif st.session_state.mode == "📚 Study Helper":

    title = "Study <span>Helper</span>"
    subtitle = "Learn faster with explanations, quizzes and study tools."
    badge = "📚 STUDY MODE"

else:

    title = "Gaming <span>Helper</span>"
    subtitle = "Strategies, builds, settings and gaming advice."
    badge = "🎮 GAMING MODE"

# IMPORTANT:
# Use st.html instead of st.markdown for HTML UI.

st.html(
    f"""
    <div class="app-header">

        <div class="app-logo">🔥</div>

        <h1 class="app-title">
            {title}
        </h1>

        <div class="app-subtitle">
            {subtitle}
        </div>

        <div class="mode-badge">
            {badge}
        </div>

    </div>
    """
)

# ============================================================
# WELCOME
# ============================================================

if not st.session_state.messages:

    if st.session_state.mode == "🤖 Chill Bro Chat":

        icon = "🤖"
        welcome_title = "What can I help you with?"
        welcome_text = (
            "Ask questions, brainstorm ideas, learn something new, "
            "or just chat."
        )

    elif st.session_state.mode == "📚 Study Helper":

        icon = "📚"
        welcome_title = "Ready to study?"
        welcome_text = (
            "Ask me to explain a topic, make a quiz, create "
            "flashcards, or build a study plan."
        )

    else:

        icon = "🎮"
        welcome_title = "Ready to level up?"
        welcome_text = (
            "Ask about strategies, loadouts, sensitivity, builds, "
            "missions, bosses or game recommendations."
        )

    st.html(
        f"""
        <div class="welcome-card">

            <div class="welcome-icon">
                {icon}
            </div>

            <div class="welcome-title">
                {welcome_title}
            </div>

            <div class="welcome-text">
                {welcome_text}
            </div>

        </div>
        """
    )

# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt():

    language = st.session_state.language
    mode = st.session_state.mode

    prompt = (
        "You are Chill Bro AI.\n"
        f"Respond primarily in {language} unless the user requests another language.\n"
        "Be helpful, accurate, natural and concise.\n"
        "Do not pretend to know information you do not know.\n"
        f"Current mode: {mode}\n"
    )

    if mode == "🤖 Chill Bro Chat":

        prompt += (
            "\nPersonality:\n"
            + PERSONALITIES[st.session_state.personality]
            + "\nTalk naturally like a bro.\n"
        )

    elif mode == "📚 Study Helper":

        prompt += (
            "\nAct as a study assistant.\n"
            f"Selected tool: {st.session_state.study_tool}\n"
            "Explain difficult concepts simply.\n"
            "Use examples and structured answers.\n"
            "For quizzes, separate questions and answers.\n"
            "For flashcards, use question/answer format.\n"
            "For study plans, make realistic schedules.\n"
        )

    else:

        prompt += (
            "\nAct as a gaming assistant.\n"
            f"Selected tool: {st.session_state.gaming_tool}\n"
            "Help with gameplay, strategies, builds, loadouts, "
            "weapons, characters, maps, missions, quests, bosses, "
            "settings, sensitivity, ranks and optimization.\n"
            "If advice depends on a game version or patch, say so.\n"
            "Do not help with cheating, malware, account theft or "
            "harmful attacks against real people.\n"
        )

    return prompt

# ============================================================
# API KEY
# ============================================================

def get_api_key():

    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.environ.get("OPENAI_API_KEY")

# ============================================================
# OPENAI
# ============================================================

def ask_ai(user_message):

    api_key = get_api_key()

    if not api_key:

        return (
            "⚠️ `OPENAI_API_KEY` is missing. "
            "Add it in Streamlit Secrets."
        )

    conversation = []

    for message in st.session_state.messages[-20:]:

        conversation.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    conversation.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    payload = {
        "model": MODEL,
        "instructions": build_system_prompt(),
        "input": conversation,
    }

    try:

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )

        if response.status_code != 200:

            try:

                data = response.json()

                error_message = (
                    data
                    .get("error", {})
                    .get("message", response.text)
                )

            except Exception:

                error_message = response.text

            return f"⚠️ OpenAI error: {error_message}"

        data = response.json()

        if data.get("output_text"):
            return data["output_text"]

        collected = []

        for item in data.get("output", []):

            if item.get("type") != "message":
                continue

            for content in item.get("content", []):

                if content.get("type") == "output_text":

                    value = content.get("text", "")

                    if value:
                        collected.append(value)

        result = "\n".join(collected).strip()

        if result:
            return result

        return "⚠️ The AI returned an empty response."

    except requests.exceptions.Timeout:

        return "⏳ The request timed out. Try again."

    except requests.exceptions.RequestException as error:

        return f"🌐 Connection error: {error}"

    except Exception as error:

        return f"⚠️ Something went wrong: {error}"

# ============================================================
# CHAT
# ============================================================

for message in st.session_state.messages:

    content = (
        html.escape(message["content"])
        .replace("\n", "<br>")
    )

    if message["role"] == "user":

        st.html(
            f"""
            <div class="chat-row user">
                <div class="chat-bubble user-bubble">
                    {content}
                </div>
            </div>
            """
        )

    else:

        st.html(
            f"""
            <div class="chat-row ai">
                <div class="chat-bubble ai-bubble">
                    {content}
                </div>
            </div>
            """
        )

# ============================================================
# INPUT
# ============================================================

if st.session_state.mode == "📚 Study Helper":

    placeholder = "Ask your study question..."

elif st.session_state.mode == "🎮 Gaming Helper":

    placeholder = "Ask your gaming question..."

else:

    placeholder = "Message Chill Bro AI..."

user_input = st.chat_input(placeholder)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.spinner("Thinking..."):

        answer = ask_ai(user_input)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        🔥 Chill Bro AI • Chat • Study • Gaming • 100+ Languages
    </div>
    """
)
