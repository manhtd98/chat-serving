import streamlit as st
import random
import time
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from logging_helper import configure_logging
import requests
import os
import logging

configure_logging()

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://api:8000")
st.set_page_config(page_title="Streamlit Chat", layout="wide")
with open("./config.yml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)


def intro():
    st.title("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        """
    )



def chat_screen():
    

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            start_time = time.perf_counter()
            try:
                request_response = requests.post(
                    API_ENDPOINT + "/api/v1/chat/query",
                    json={"query": prompt, "bucket": "user1", "token": "token_id"},
                )
                response = request_response.json()
                if response:
                    assistant_response = response["result"]["answern"]
                else:
                    assistant_response = "Vui lòng đổi câu hỏi"
            except Exception as exception:
                logging.error(str(exception))
                assistant_response = "Hệ thống đang gặp lỗi, vui lòng thử lại sau"
            logging.info(f"CALLING API ENDPOINT: {time.perf_counter()-start_time}")

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

page_names_to_funcs = {
    "Sổ tay học viên": chat_screen,
    "Giáo viên": chat_screen,
    "Quy định": chat_screen,
    "Giới thiệu về phần mềm": intro
}

if __name__ == "__main__":
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status:
        
        demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
        authenticator.logout("Logout", "main", key="unique_key")
        st.sidebar.write(f"Welcome *{name}*")
        st.sidebar.title("HVKTQS Chat QA App")
        page_names_to_funcs[demo_name]()
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
