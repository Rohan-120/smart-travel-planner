"""
Streamlit Frontend — Smart Travel Planning Assistant
Provides: Login screen, Chat interface, Itinerary display
"""
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Travel Planner", page_icon="✈️", layout="wide")


def login_screen():
    st.title("Smart Travel Planning Assistant")
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # TODO: call POST /auth/login and store session
        st.error("Login not yet implemented")


def chat_interface():
    st.title("Travel Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me about your next trip..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # TODO: call backend agent endpoint and stream response
        with st.chat_message("assistant"):
            st.markdown("Agent response coming soon...")


def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_screen()
    else:
        chat_interface()


if __name__ == "__main__":
    main()
