import streamlit as st
import edge_tts
import asyncio
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(
page_title="Text to Speech & Translation",
page_icon="🎙️",
layout="centered"
)

st.title("🎙️ Text to Speech & Translation Demo by Raj")

lang_map = {
"English": "en",
"Hindi": "hi",
"Tamil": "ta",
"Thai": "th",
"Odia": "or",
"Kannada": "kn"
}

voice_map = {
"English": {
"Male": "en-US-GuyNeural",
"Female": "en-US-JennyNeural"
},
"Hindi": {
"Male": "hi-IN-MadhurNeural",
"Female": "hi-IN-SwaraNeural"
},
"Tamil": {
"Male": "ta-IN-ValluvarNeural",
"Female": "ta-IN-PallaviNeural"
},
"Thai": {
"Male": "th-TH-NiwatNeural",
"Female": "th-TH-PremwadeeNeural"
},
"Odia": {
"Male": "en-US-GuyNeural",
"Female": "en-US-JennyNeural"
},
"Kannada": {
"Male": "kn-IN-GaganNeural",
"Female": "kn-IN-SapnaNeural"
}
}

input_lang = st.selectbox(
"Input Language",
list(lang_map.keys())
)

output_lang = st.selectbox(
"Output Language",
list(lang_map.keys())
)

voice_gender = st.selectbox(
"Select Voice",
["Male", "Female"]
)

text = st.text_area(
"Enter Text",
placeholder="Type something here..."
)

def translate_text(text, src_lang, tgt_lang):
if src_lang == tgt_lang:
return text

```
translator = GoogleTranslator(
    source=src_lang,
    target=tgt_lang
)

return translator.translate(text)
```

async def generate_audio(text, voice):
communicate = edge_tts.Communicate(
text=text,
voice=voice
)

```
audio_data = b""

async for chunk in communicate.stream():
    if chunk["type"] == "audio":
        audio_data += chunk["data"]

return BytesIO(audio_data)
```

def text_to_speech(text, voice):
return asyncio.run(
generate_audio(text, voice)
)

if st.button("Translate & Speak"):

```
if not text.strip():
    st.warning("Please enter some text.")

else:
    try:
        src_code = lang_map[input_lang]
        tgt_code = lang_map[output_lang]

        translated_text = translate_text(
            text,
            src_code,
            tgt_code
        )

        st.subheader("Translated Text")
        st.write(translated_text)

        selected_voice = voice_map[
            output_lang
        ][voice_gender]

        audio_file = text_to_speech(
            translated_text,
            selected_voice
        )

        st.subheader("Audio")
        st.audio(
            audio_file,
            format="audio/mp3"
        )

        audio_file.seek(0)

        st.download_button(
            label="⬇ Download MP3",
            data=audio_file,
            file_name="translated_speech.mp3",
            mime="audio/mpeg"
        )

        st.success(
            f"Speech generated successfully in {output_lang} ({voice_gender})"
        )

    except Exception as e:
        st.error(f"Error: {e}")
```

st.markdown("---")
st.caption("Made by Raj")
