import streamlit as st
import openai
import tempfile
import os
from elevenlabs import set_api_key, generate, save

# Clés API depuis les secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

st.set_page_config("🎧 Podcast Interactif", layout="centered")
st.title("🎧 Épisode interactif : Israël - Iran")

# Écoute du podcast
st.subheader("🎙 Écoutez le podcast")
audio_file = "podcast.mp3"
st.audio(audio_file, format="audio/mp3")

# Posez votre question vocalement
st.subheader("❓ Posez une question à l’oral")
uploaded_audio = st.file_uploader("Enregistrez-vous (format .wav)", type=["wav"])

if uploaded_audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_audio.read())
        tmp_path = tmp.name

    with st.spinner("⏳ Transcription en cours..."):
        transcript = openai.Audio.transcribe("whisper-1", tmp_path)
        st.markdown(f"📝 **Transcription** : {transcript['text']}")

        with st.spinner("🤖 Génération de la réponse..."):
            completion = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Tu es un expert en géopolitique et tu expliques de manière simple."},
                    {"role": "user", "content": transcript["text"]}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(f"💬 **Réponse IA** : {answer}")

        with st.spinner("🔊 Synthèse vocale..."):
            audio = generate(text=answer, voice="Bella", model="eleven_multilingual_v1")
            save(audio, "response.mp3")
            st.audio("response.mp3", format="audio/mp3")
