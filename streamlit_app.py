import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="RAG Chat", page_icon="🤖")
st.title("📚 Dokument-Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Stelle eine Frage zum Dokument..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherchiere..."):
            try:
                url = f"{BACKEND_URL}/ask"
                resp = requests.post(
                    url,
                    json={"question": prompt, "top_k": 3},
                    timeout=90
                )

                if resp.status_code != 200:
                    answer = f"Backend error {resp.status_code}: {resp.text}"
                else:
                    answer = resp.json()["answer"]

            except Exception as e:
                answer = f"Fehler: {e}"

        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})