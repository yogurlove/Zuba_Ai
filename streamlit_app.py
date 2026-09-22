import streamlit as st
import requests
import base64
import os
import html

# ============================================================
# 🎮🔥 CHILL BRO AI — ALL-IN-ONE STREAMLIT APP
# ============================================================

st.set_page_config(
    page_title="Chill Bro AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONFIG
# ============================================================

MODEL = "gpt-5.6-luna"

LANGUAGES = [
    "English", "Hindi", "Punjabi", "Nepali", "Urdu", "Bengali",
    "Tamil", "Telugu", "Marathi", "Gujarati", "Kannada",
    "Malayalam", "Odia", "Assamese", "French", "Spanish",
    "German", "Italian", "Portuguese", "Russian", "Arabic",
    "Chinese", "Japanese", "Korean", "Turkish", "Indonesian"
]

PERSONALITIES = {
    "😎 Chill Bro":
        "Relaxed, friendly, funny and casual like a cool friend.",

    "😂 Funny":
        "Humorous, playful and entertaining.",

    "🧠 Smart":
        "Intelligent, clear, precise and educational.",

    "❤️ Lovely":
        "Warm, kind, positive and supportive.",

    "🤝 Best Friend":
        "Talk naturally like a close best friend. Casual, honest and supportive.",

    "💀 Extreme Toxic":
        """
        Use a chaotic, profanity-heavy fictional bro-style personality.
        Strong profanity and vulgar slang are allowed for playful trash-talk.
        You may use words such as fuck, shit, damn, dumbass and similar
        exaggerated insults.

        Keep it playful and non-threatening.
        Do not use hateful slurs.
        Do not threaten violence.
        Do not encourage real-world harassment.
        Do not target protected groups.
        Do not turn the conversation into genuine abuse.
        """
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
    "🌌 Neon Night": ("#070016", "#00eaff", "#ff00e6"),
    "🌈 Rainbow": ("#12001f", "#ff00aa", "#00ffff"),
    "💜 Purple Dream": ("#10001c", "#b700ff", "#ff4fd8"),
    "🌊 Ocean": ("#00131c", "#00e5ff", "#008cff"),
    "💚 Matrix": ("#001008", "#00ff66", "#00cc44"),
    "🌅 Sunset": ("#21000c", "#ff5e00", "#ff0066"),
    "💗 Pink Candy": ("#21000f", "#ff4da6", "#ff99cc"),
    "❄️ Ice": ("#00141f", "#8ffcff", "#4da6ff"),
    "🔥 Fire": ("#200500", "#ff5e00", "#ffcc00"),
    "🖤 Dark": ("#050505", "#ffffff", "#888888"),
    "🤍 Light": ("#f4f4f4", "#111111", "#666666"),
}

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "🌌 Neon Night"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "personality" not in st.session_state:
    st.session_state.personality = "😎 Chill Bro"

if "mode" not in st.session_state:
    st.session_state.mode = "🤖 Chill Bro Chat"

if "music_on" not in st.session_state:
    st.session_state.music_on = False

if "music_volume" not in st.session_state:
    st.session_state.music_volume = 0.25

if "sound_on" not in st.session_state:
    st.session_state.sound_on = False

if "stickers_on" not in st.session_state:
    st.session_state.stickers_on = True

if "gif_on" not in st.session_state:
    st.session_state.gif_on = True

# ============================================================
# THEME
# ============================================================

bg, primary, secondary = THEMES[st.session_state.theme]

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
            radial-gradient(circle at 15% 20%, {primary}22 0%, transparent 28%),
            radial-gradient(circle at 85% 80%, {secondary}22 0%, transparent 28%),
            linear-gradient(135deg, {bg}, #03030a 70%);
        color: white;
    }}

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(180deg, {bg}, #03030a);
        border-right: 1px solid {primary}55;
    }}

    .main-title {{
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        color: {primary};
        text-shadow:
            0 0 8px {primary},
            0 0 20px {primary},
            0 0 40px {secondary};
        animation: titleGlow 2s infinite alternate;
    }}

    .subtitle {{
        text-align: center;
        color: white;
        font-size: 18px;
        opacity: .85;
        margin-bottom: 20px;
    }}

    .anime-face {{
        width: 110px;
        height: 110px;
        margin: 10px auto 20px auto;
        border-radius: 50%;
        background:
            radial-gradient(circle at 35% 35%, white 0 4%, transparent 5%),
            radial-gradient(circle at 65% 35%, white 0 4%, transparent 5%),
            linear-gradient(145deg, {primary}, {secondary});
        border: 4px solid white;
        box-shadow:
            0 0 15px {primary},
            0 0 35px {secondary};
        animation: floatFace 2.5s infinite ease-in-out;
        position: relative;
    }}

    .anime-face:after {{
        content: "⌣";
        position: absolute;
        left: 39px;
        top: 52px;
        font-size: 30px;
        color: white;
    }}

    .energy-ring {{
        width: 145px;
        height: 145px;
        border-radius: 50%;
        border: 2px solid {primary};
        margin: -138px auto 35px auto;
        opacity: .5;
        animation: ring 2s infinite linear;
    }}

    .chat-card {{
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        border: 1px solid {primary}44;
        background: rgba(255,255,255,.04);
        animation: messageIn .35s ease;
    }}

    .user-card {{
        border-left: 4px solid {secondary};
    }}

    .assistant-card {{
        border-left: 4px solid {primary};
    }}

    .thinking {{
        color: {primary};
        font-weight: bold;
        animation: pulse 1s infinite;
    }}

    .sticker {{
        display: inline-block;
        font-size: 35px;
        animation: sticker 1.8s infinite ease-in-out;
        margin: 5px;
    }}

    .gaming-box {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid {primary}66;
        background: linear-gradient(135deg, {primary}12, {secondary}12);
        box-shadow: 0 0 25px {primary}22;
        margin-bottom: 15px;
    }}

    @keyframes titleGlow {{
        from {{
            text-shadow: 0 0 8px {primary};
        }}
        to {{
            text-shadow:
                0 0 10px {primary},
                0 0 30px {secondary},
                0 0 50px {primary};
        }}
    }}

    @keyframes floatFace {{
        0%,100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}

    @keyframes ring {{
        from {{ transform: rotate(0deg) scale(.9); }}
        to {{ transform: rotate(360deg) scale(1.05); }}
    }}

    @keyframes messageIn {{
        from {{
            opacity: 0;
            transform: translateY(8px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes pulse {{
        0%,100% {{ opacity: .35; }}
        50% {{ opacity: 1; }}
    }}

    @keyframes sticker {{
        0%,100% {{ transform: rotate(-8deg) scale(1); }}
        50% {{ transform: rotate(8deg) scale(1.15); }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔥 Chill Bro AI")

    mode = st.radio(
        "Choose Mode",
        [
            "🤖 Chill Bro Chat",
            "📚 Study Helper",
            "🎮 Gaming Helper",
        ],
        index=[
            "🤖 Chill Bro Chat",
            "📚 Study Helper",
            "🎮 Gaming Helper",
        ].index(st.session_state.mode),
    )

    st.session_state.mode = mode

    st.markdown("---")

    st.session_state.theme = st.selectbox(
        "🎨 Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
    )

    if st.session_state.theme == "🎨 Custom":
        pass

    st.session_state.language = st.selectbox(
        "🌍 Language",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language),
    )

    if mode == "🤖 Chill Bro Chat":

        st.session_state.personality = st.selectbox(
            "🎭 Personality",
            list(PERSONALITIES.keys()),
            index=list(PERSONALITIES.keys()).index(
                st.session_state.personality
            ),
        )

    elif mode == "📚 Study Helper":

        st.session_state.study_tool = st.selectbox(
            "📚 Study Tool",
            STUDY_TOOLS,
        )

    else:

        st.session_state.gaming_tool = st.selectbox(
            "🎮 Gaming Tool",
            GAMING_TOOLS,
        )

    st.markdown("---")

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 🎵 Background Music")

    st.session_state.music_on = st.toggle(
        "🎧 Golden Brown Instrumental",
        value=st.session_state.music_on,
    )

    st.session_state.music_volume = st.slider(
        "🔊 Volume",
        0.0,
        1.0,
        st.session_state.music_volume,
        0.05,
    )

    st.session_state.sound_on = st.toggle(
        "⚡ Anime Sound",
        value=st.session_state.sound_on,
    )

    st.session_state.stickers_on = st.toggle(
        "✨ Animated Stickers",
        value=st.session_state.stickers_on,
    )

    st.session_state.gif_on = st.toggle(
        "🎬 Anime GIF",
        value=st.session_state.gif_on,
    )

# ============================================================
# AUDIO
# ============================================================

def play_local_audio(filename, autoplay=False, loop=False, volume=0.5):
    if not os.path.exists(filename):
        return

    try:
        with open(filename, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        mime = "audio/mpeg"

        auto = "autoplay" if autoplay else ""
        loop_attr = "loop" if loop else ""

        st.markdown(
            f"""
            <audio controls {auto} {loop_attr}
                style="width:100%;"
                volume="{volume}">
                <source src="data:{mime};base64,{data}" type="{mime}">
            </audio>
            <script>
            const audios = document.querySelectorAll("audio");
            audios.forEach(a => {{
                a.volume = {volume};
            }});
            </script>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass


if st.session_state.music_on:
    play_local_audio(
        "golden_brown.mp3",
        autoplay=True,
        loop=True,
        volume=st.session_state.music_volume,
    )

if st.session_state.sound_on:
    play_local_audio(
        "anime_power.mp3",
        autoplay=True,
        loop=False,
        volume=0.35,
    )

# ============================================================
# HEADER
# ============================================================

if st.session_state.mode == "🤖 Chill Bro Chat":
    title = "🔥 Chill Bro AI"
    subtitle = "⚡ Your anime-powered AI bro 😎"

elif st.session_state.mode == "📚 Study Helper":
    title = "📚 Study Helper"
    subtitle = "✨ Train your brain like an anime protagonist 🧠🔥"

else:
    title = "🎮 Gaming Helper"
    subtitle = "⚔️ Level up your gaming skills, bro 🔥"

st.markdown(
    f'<div class="main-title">{title}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="subtitle">{subtitle}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="anime-face"></div>', unsafe_allow_html=True)
st.markdown('<div class="energy-ring"></div>', unsafe_allow_html=True)

if st.session_state.stickers_on:
    st.markdown(
        """
        <div style="text-align:center;">
            <span class="sticker">🔥</span>
            <span class="sticker">⚡</span>
            <span class="sticker">🎮</span>
            <span class="sticker">😎</span>
            <span class="sticker">💀</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.gif_on:
    st.markdown(
        """
        <div style="text-align:center;margin:10px;">
            <img
                src="https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif"
                width="180"
                style="border-radius:20px;"
            >
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt():

    language = st.session_state.language

    base = f"""
You are Chill Bro AI.

Always communicate primarily in {language} unless the user asks for another language.

You are helpful, entertaining, friendly and concise.

Never pretend to have information you do not have.

Current application mode:
{st.session_state.mode}
"""

    if st.session_state.mode == "🤖 Chill Bro Chat":

        personality = PERSONALITIES[
            st.session_state.personality
        ]

        base += f"""

Personality:
{personality}

Talk naturally like a bro.
Use emojis occasionally.
"""

    elif st.session_state.mode == "📚 Study Helper":

        tool = getattr(
            st.session_state,
            "study_tool",
            "📖 Explain Topic",
        )

        base += f"""

You are currently acting as a study assistant.

Selected study tool:
{tool}

Give clear explanations.
Use examples.
Break difficult concepts into simple steps.
For quizzes, provide questions and answers separately when useful.
For flashcards, use question/answer format.
For study plans, make realistic schedules.
"""

    else:

        tool = getattr(
            st.session_state,
            "gaming_tool",
            "🎯 Game Tips",
        )

        base += f"""

You are currently acting as a gaming assistant.

Selected gaming tool:
{tool}

Help with:
- gameplay strategy
- builds
- loadouts
- weapons
- characters
- maps
- missions
- quests
- bosses
- sensitivity
- controls
- rank improvement
- PC/mobile optimization
- game recommendations

If a game has different patches or versions, mention that exact current
version information may matter rather than pretending old information is current.

Do not help with cheating, malware, account theft, exploits against real
people, or other harmful activity.
"""

    return base


# ============================================================
# OPENAI API
# ============================================================

def get_api_key():

    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.environ.get("OPENAI_API_KEY")


def ask_ai(user_message):

    api_key = get_api_key()

    if not api_key:
        return (
            "⚠️ Bro, `OPENAI_API_KEY` is missing. "
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
                error_data = response.json()
                error_message = error_data.get(
                    "error",
                    {}
                ).get(
                    "message",
                    response.text
                )
            except Exception:
                error_message = response.text

            return f"⚠️ OpenAI error: {error_message}"

        data = response.json()

        if data.get("output_text"):
            return data["output_text"]

        output = data.get("output", [])

        collected = []

        for item in output:

            if item.get("type") != "message":
                continue

            for content in item.get("content", []):

                if content.get("type") == "output_text":
                    collected.append(
                        content.get("text", "")
                    )

        result = "\n".join(collected).strip()

        if result:
            return result

        return "⚠️ Bro, the AI returned an empty response."

    except requests.exceptions.Timeout:
        return "⏳ Bro, the AI took too long. Try again."

    except requests.exceptions.RequestException as e:
        return f"🌐 Connection error: {e}"

    except Exception as e:
        return f"💀 Something went wrong: {e}"


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    if role == "user":
        avatar = "😎"
        label = "You"
        card_class = "user-card"
    else:
        avatar = "🔥"
        label = "Chill Bro AI"
        card_class = "assistant-card"

    safe_content = html.escape(message["content"]).replace(
        "\n",
        "<br>"
    )

    st.markdown(
        f"""
        <div class="chat-card {card_class}">
            <b>{avatar} {label}</b>
            <div style="margin-top:6px;">
                {safe_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CHAT INPUT
# ============================================================

placeholder = "Ask anything, bro... 🔥"

if st.session_state.mode == "📚 Study Helper":
    placeholder = "Ask your study question... 📚"

elif st.session_state.mode == "🎮 Gaming Helper":
    placeholder = "Ask your gaming question... 🎮"

user_input = st.chat_input(placeholder)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    st.markdown(
        f"""
        <div class="chat-card user-card">
            <b>😎 You</b>
            <div style="margin-top:6px;">
                {html.escape(user_input)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("⚡ Bro is thinking..."):

        answer = ask_ai(user_input)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.markdown(
        f"""
        <div class="chat-card assistant-card">
            <b>🔥 Chill Bro AI</b>
            <div style="margin-top:6px;">
      
