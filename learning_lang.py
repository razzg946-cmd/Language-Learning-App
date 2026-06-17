import streamlit as st
from deep_translator import GoogleTranslator
from io import BytesIO
import edge_tts
import asyncio

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Rvoice - Translate & Speak",
    page_icon="🎙️",
    layout="centered"
)

# -----------------------
# Title
# -----------------------
st.title("🎙️ Rvoice - Text to Speech & Translation DEMO")
st.write("Translate text and convert it into natural AI voice speech")

# -----------------------
# Language Map
# -----------------------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Odia": "or",
    "Assamese": "as",
    "Nepali": "ne",
    "Kashmiri": "ks",
    "Manipuri": "mni",
    "Mizo": "lus",
    "Urdu": "ur",
    "Thai": "th",
    "Chinese (Mandarin)": "zh-CN"
}

# -----------------------
# Voice Map
# -----------------------
voice_map = {
    "English": {"Male": "en-US-GuyNeural", "Female": "en-US-JennyNeural"},
    "Hindi": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Tamil": {"Male": "ta-IN-ValluvarNeural", "Female": "ta-IN-PallaviNeural"},
    "Telugu": {"Male": "te-IN-MohanNeural", "Female": "te-IN-ShrutiNeural"},
    "Kannada": {"Male": "kn-IN-GaganNeural", "Female": "kn-IN-SapnaNeural"},
    "Malayalam": {"Male": "ml-IN-MidhunNeural", "Female": "ml-IN-SobhanaNeural"},
    "Marathi": {"Male": "mr-IN-ManoharNeural", "Female": "mr-IN-AarohiNeural"},
    "Gujarati": {"Male": "gu-IN-NiranjanNeural", "Female": "gu-IN-DhwaniNeural"},
    "Bengali": {"Male": "bn-IN-BashkarNeural", "Female": "bn-IN-TanishaaNeural"},
    "Urdu": {"Male": "ur-PK-AsadNeural", "Female": "ur-PK-UzmaNeural"},
    "Thai": {"Male": "th-TH-NiwatNeural", "Female": "th-TH-PremwadeeNeural"},
    "Chinese (Mandarin)": {
        "Male": "zh-CN-YunxiNeural",
        "Female": "zh-CN-XiaoxiaoNeural"
    },

    # Fallback Languages
    "Punjabi": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Odia": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Assamese": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Nepali": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Kashmiri": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Manipuri": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "Mizo": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
}

# -----------------------
# Safe Voice Getter
# -----------------------
def get_voice(lang, gender):
    try:
        return voice_map[lang][gender]
    except:
        if gender == "Male":
            return "hi-IN-MadhurNeural"
        return "hi-IN-SwaraNeural"

# -----------------------
# Translation
# -----------------------
def translate_text(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text

    try:
        translator = GoogleTranslator(
            source=src_lang,
            target=tgt_lang
        )
        return translator.translate(text)
    except:
        return text

# -----------------------
# TTS
# -----------------------
async def generate_audio(text, voice):
    audio_data = b""

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    return BytesIO(audio_data)

def text_to_speech(text, voice_gender, output_lang):
    try:
        voice = get_voice(output_lang, voice_gender)
        return asyncio.run(generate_audio(text, voice))

    except:
        try:
            # Hindi fallback
            fallback = (
                "hi-IN-MadhurNeural"
                if voice_gender == "Male"
                else "hi-IN-SwaraNeural"
            )

            return asyncio.run(
                generate_audio(text, fallback)
            )

        except:
            try:
                # English fallback
                fallback = (
                    "en-US-GuyNeural"
                    if voice_gender == "Male"
                    else "en-US-JennyNeural"
                )

                return asyncio.run(
                    generate_audio(text, fallback)
                )

            except:
                return None

# -----------------------
# UI
# -----------------------
input_lang = st.selectbox(
    "Input Language",
    list(lang_map.keys())
)

output_lang = st.selectbox(
    "Output Language",
    list(lang_map.keys())
)

voice_gender = st.selectbox(
    "Voice Type",
    ["Male", "Female"]
)

text = st.text_area(
    "Enter Text",
    placeholder="Type something..."
)

# -----------------------
# Button
# -----------------------
if st.button("Translate & Speak"):

    if not text.strip():
        st.warning("Please enter text first!")

    else:

        try:
            src_code = lang_map[input_lang]
            tgt_code = lang_map[output_lang]

            with st.spinner("Translating..."):
                translated_text = translate_text(
                    text,
                    src_code,
                    tgt_code
                )

            st.subheader("Translated Text")
            st.write(translated_text)

            unsupported = [
                "Punjabi",
                "Odia",
                "Assamese",
                "Nepali",
                "Kashmiri",
                "Manipuri",
                "Mizo"
            ]

            if output_lang in unsupported:
                st.info(
                    f"{output_lang} native voice unavailable. "
                    f"Using Hindi AI voice."
                )

            with st.spinner("Generating Voice..."):
                audio_file = text_to_speech(
                    translated_text,
                    voice_gender,
                    output_lang
                )

            if audio_file:

                st.subheader("Audio Output")

                st.audio(
                    audio_file,
                    format="audio/mp3"
                )

                audio_file.seek(0)

                st.download_button(
                    label="⬇ Download MP3",
                    data=audio_file,
                    file_name="rvoice_output.mp3",
                    mime="audio/mpeg"
                )

                st.success(
                    "Voice generated successfully!"
                )

            else:
                st.error(
                    "Voice generation failed."
                )

        except Exception as e:
            st.error(
                f"Error: {str(e)}"
            )

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Rvoice © Founder - Raj Gupta")
