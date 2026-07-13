# streamlit_agent.py
import os
import tempfile

import streamlit as st

from agent_loop import run_agent
from kb_core import add_note, add_note_from_audio


st.set_page_config(
    page_title="Meine Wissensdatenbank",
    page_icon="🧠",
)

st.title("🧠 Persönlicher Wissensassistent")


if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Notiz hinzufügen")

    note_text = st.text_area("Text eingeben")
    note_tags = st.text_input("Tags (kommagetrennt)")

    if st.button("Speichern", use_container_width=True):
        if not note_text.strip():
            st.warning("Bitte gib zuerst einen Text ein.")
        else:
            try:
                tags = [
                    tag.strip()
                    for tag in note_tags.split(",")
                    if tag.strip()
                ]

                add_note(
                    text=note_text,
                    tags=tags,
                )

                st.success("Gespeichert!")

            except Exception as error:
                st.error(f"Die Notiz konnte nicht gespeichert werden: {error}")

    st.divider()

    audio_file = st.file_uploader(
        "Audio-Notiz",
        type=["mp3", "wav", "m4a"],
    )

    audio_tags = st.text_input(
        "Audio-Tags (kommagetrennt)",
        key="audio_tags",
    )

    if st.button(
        "Transkribieren & Speichern",
        use_container_width=True,
    ):
        if audio_file is None:
            st.warning("Bitte lade zuerst eine Audiodatei hoch.")
        else:
            suffix = os.path.splitext(audio_file.name)[1] or ".wav"
            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:
                    temp_file.write(audio_file.getbuffer())
                    temp_path = temp_file.name

                tags = [
                    tag.strip()
                    for tag in audio_tags.split(",")
                    if tag.strip()
                ]

                result = add_note_from_audio(
                    audio_path=temp_path,
                    tags=tags,
                )

                st.success(
                    f"Notiz gespeichert: {result['content'][:60]}..."
                )

            except Exception as error:
                st.error(
                    f"Die Audio-Notiz konnte nicht gespeichert werden: {error}"
                )

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

    st.divider()

    if st.button("Chat löschen", use_container_width=True):
        st.session_state.history = []
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


prompt = st.chat_input("Frage an deine Wissensbasis...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent denkt..."):
            try:
                answer, updated_history = run_agent(
                    prompt,
                    st.session_state.history,
                )

                st.session_state.history = updated_history
                st.write(answer)

            except Exception as error:
                answer = (
                    "Der Agent konnte die Anfrage nicht verarbeiten. "
                    f"Fehler: {error}"
                )
                st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )