# app.py

from translator import translate_text, detect_language
from speech_utils import text_to_speech
import os
import streamlit as st

# ── Session‑state defaults ────────────────────────────────────────────────────
if "source_lang" not in st.session_state: st.session_state.source_lang = "English"
if "target_lang" not in st.session_state: st.session_state.target_lang = "Hindi"
if "swap_triggered" not in st.session_state: st.session_state.swap_triggered = False
if "theme" not in st.session_state: st.session_state.theme = "Light"

# ── Language Mapping ───────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect": "auto", "Arabic": "ar", "Bengali": "bn", "Chinese (Simplified)": "zh-cn",
    "English": "en", "French": "fr", "German": "de", "Gujarati": "gu", "Hindi": "hi",
    "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Korean": "ko", "Marathi": "mr",
    "Odia": "or", "Punjabi": "pa", "Russian": "ru", "Spanish": "es", "Tamil": "ta",
    "Telugu": "te", "Urdu": "ur"
}
LANGUAGE_CODES_TO_NAMES = {v: k for k, v in LANGUAGES.items()}

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Smart Language Translator", page_icon="🌐", layout="wide")

# ── Theme Styling ──────────────────────────────────────────────────────────────
if st.session_state.theme == "Dark":
    text_color = "white"
    st.markdown("""
        <style>
        .stApp { background:#121212; color:#fff; font-family:'Segoe UI'; }
        div.stButton>button { background:#333; color:#fff; border:1px solid #555; }
        div.stButton>button:hover { background:#444; }
        textarea,div[data-baseweb="select"]{background:#1e1e1e!important;color:#fff!important;border:1px solid #444!important;}
        textarea::placeholder{color:#888!important;}
        .msg{width:100%;padding:10px;border-radius:5px;margin-top:10px;}
        .warning{background:#fff3cd;color:#856404;border:1px solid #ffeeba;}
        .error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb;}
        </style>
    """, unsafe_allow_html=True)
else:
    text_color = "black"
    st.markdown("""
        <style>
        .stApp { background:#f9f9f9; color:#000; font-family:'Segoe UI'; }
        div.stButton>button { background:#fff; color:#000; border:1.5px solid #444; }
        div.stButton>button:hover { background:#f0f0f0; border-color:#222; }
        textarea{background:#fff!important;color:#000!important;border:1px solid #ccc!important;}
        textarea::placeholder{color:#666!important;}
        .msg{width:100%;padding:10px;border-radius:5px;margin-top:10px;}
        .warning{background:#fff3cd;color:#856404;border:1px solid #ffeeba;}
        .error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb;}
        </style>
    """, unsafe_allow_html=True)

# ── Header and Theme Toggle ────────────────────────────────────────────────────
col_title, col_toggle = st.columns([10,1])
with col_title:
    st.markdown("### 🌐 Smart Language Translator")
with col_toggle:
    icon = "🌙" if st.session_state.theme == "Light" else "☀️"
    if st.button(icon, key="theme_toggle"):
        st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
        st.rerun()

st.markdown("<p style='font-size:16px;color:gray;'>Translate text effortlessly with a modern, voice‑enabled translator app.</p>", unsafe_allow_html=True)

# Divider
st.markdown(f"""<div style='height:3px;width:100%;background:{'#fff' if st.session_state.theme=='Dark' else '#000'};margin:1.5rem 0;border-radius:2px;'></div>""", unsafe_allow_html=True)

# ── Handle Swap ───────────────────────────────────────────────────────────────
if st.session_state.swap_triggered:
    st.session_state.source_lang, st.session_state.target_lang = st.session_state.target_lang, st.session_state.source_lang
    st.session_state.swap_triggered = False

# ── Language Selection ────────────────────────────────────────────────────────
col_from, col_swap, col_to = st.columns([5,1,5])

with col_from:
    st.markdown("**From**")
    st.session_state.source_lang = st.selectbox(
        "", list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.source_lang),
        key="src_lang_selectbox"
    )

with col_swap:
    if st.button("🔁", key="swap_btn"):
        st.session_state.swap_triggered = True
        st.rerun()

with col_to:
    st.markdown("**To**")
    st.session_state.target_lang = st.selectbox(
        "", list(LANGUAGES.keys())[1:],  # excluding Auto Detect
        index=list(LANGUAGES.keys())[1:].index(st.session_state.target_lang),
        key="dest_lang_selectbox"
    )

# ── Text Input ────────────────────────────────────────────────────────────────
text = st.text_area("✍️ Enter Text", height=200, placeholder="Type something...")

# ── Translate Button ──────────────────────────────────────────────────────────
if st.button("🚀 Translate Now"):
    if not text.strip():
        st.markdown('<div class="msg warning">⚠️ Please enter some text to translate.</div>', unsafe_allow_html=True)
    else:
        from_lang_code = LANGUAGES.get(st.session_state.source_lang, "auto")
        to_lang_code = LANGUAGES.get(st.session_state.target_lang, "en")

        # Auto-detect
        if from_lang_code == "auto":
            detected = detect_language(text)
            st.info(f"🧭 Detected Language: {LANGUAGE_CODES_TO_NAMES.get(detected, detected)}")
            from_lang_code = detected

        try:
            result = translate_text(text, to_lang_code, src=from_lang_code)
            st.markdown("### 🎯 Translated Text")
            st.success(result)

            audio_file = text_to_speech(result, to_lang_code, "translated.mp3")
            if audio_file and os.path.exists(audio_file):
                audio_bytes = open(audio_file, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
                with open(audio_file, "rb") as file:
                    st.download_button(
                        label="💾 Download Audio",
                        data=file,
                        file_name="translated_audio.mp3",
                        mime="audio/mp3"
                    )
        except Exception as e:
            st.markdown(f'<div class="msg error">❌ Translation Error: {e}</div>', unsafe_allow_html=True)
