import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO

st.title("🌐 Language Learning App by Raj")

# Language selection
input_lang = st.selectbox("Input Language:", ("English", "Hindi", "Tamil"))
output_lang = st.selectbox("Translate To:", ("English", "Hindi", "Tamil"))

# Map language names to codes
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
        st.warning("⚠️ Please enter a sentence.")
    else:
        try:
            src_code = lang_map[input_lang]
            tgt_code = lang_map[output_lang]

            translated = translate(text, src_code, tgt_code)
            st.markdown(f"**Translated Text ({output_lang}):** {translated}")

            audio_bytes = text_to_speech(translated, tgt_code)
            st.audio(audio_bytes.read(), format="audio/mp3")
            st.success("✅ Translation and speech ready!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
