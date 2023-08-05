import streamlit as st
import random
import time
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import logging
logging.basicConfig(
    handlers=[logging.StreamHandler()]
)
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
    st.title("HVKTQS Chat QA App")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    print(st.session_state.messages)
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
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
if __name__ == "__main__":
    name, authentication_status, username = authenticator.login("Login", "main")
    print(name, authentication_status, username)
    if authentication_status:
        authenticator.logout("Logout", "main", key="unique_key")
        st.write(f"Welcome *{name}*")
        chat_screen()
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")