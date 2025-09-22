import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO

st.title("Two-Way Language Learning App by Raj")

# Language selection
learn_lang = st.selectbox("Select Language to Learn:", ("Hindi", "Tamil"))
input_mode = st.radio("Type your sentence in:", ("Learning Language", "English"))

# Map languages to codes
lang_map = {"English": "en", "Hindi": "hi", "Tamil": "ta"}

# Input text
text = st.text_area("Type your sentence:")

def translate(text, src, tgt):
    if src == tgt:
        return text
    return GoogleTranslator(source=src, target=tgt).translate(text)

def text_to_speech(text, lang):
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

if st.button("Translate & Listen"):
    if not text.strip():
        st.warning(" Please enter a sentence.")
    else:
        try:
            learn_code = lang_map[learn_lang]
            eng_code = lang_map["English"]

            if input_mode == "Learning Language":
                # User types in learning language
                translated = translate(text, learn_code, eng_code)
                st.markdown(f"**{learn_lang}:** {text}")
                st.markdown(f"**English:** {translated}")
                audio_bytes = text_to_speech(text, learn_code)

            else:
                # User types in English
                translated = translate(text, eng_code, learn_code)
                st.markdown(f"**English:** {text}")
                st.markdown(f"**{learn_lang}:** {translated}")
                audio_bytes = text_to_speech(translated, learn_code)

            st.audio(audio_bytes.read(), format="audio/mp3")
            st.success(" Translation and pronunciation ready!")
        except Exception as e:
            st.error(f"Error: {e}")

