import streamlit as st
import time
import requests
import hashlib

# Hugging Face API information
HF_API_URL = "https://api-inference.huggingface.co/models/gpt-3.5-turbo"  # Use your model's URL
HF_API_TOKEN = "eieieieijeheueueueuue"  # Replace this with your Hugging Face API token

# Streamlit authentication logic (remains the same)
users = {}
def simple_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

default_password = "password123"
default_password_hash = simple_hash(default_password)
users["admin"] = default_password_hash

def authenticate(username, password):
    if username in users:
        stored_hash = users[username]
        entered_hash = simple_hash(password)
        return stored_hash == entered_hash
    return False

# Function to call Hugging Face API to generate response
def get_huggingface_response(user_input):
    headers = {
        'Authorization': f'Bearer {HF_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "inputs": user_input
    }
    
    try:
        response = requests.post(HF_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return data[0]['generated_text']  # This depends on the actual response format from the model
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    st.set_page_config(page_title="AI Help Desk", page_icon="🤖", layout="wide")

    st.markdown(""" 
    <style>
    body {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    .login-box {
        padding: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.subheader("Sign In")
        with st.container():
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            if st.button("Login", key="login"):
                if authenticate(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['current_page'] = "Home"
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()  # Use st.rerun()
                else:
                    st.error("Invalid username or password")
    else:
        st.sidebar.title("Navigation")

        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = "Home"

        page = st.sidebar.radio("Go to:", ["Home", "Claim Enquiry", "Inquiry Form"],
                                key="page_radio",
                                index=["Home", "Claim Enquiry", "Inquiry Form"].index(st.session_state['current_page']))

        if page != st.session_state['current_page']:
            st.session_state['current_page'] = page
            st.rerun()  # Use st.rerun()

        st.title(page)
        st.write(f"### Welcome to {page}!")

        if page == "Home":
            st.write("## AI Help Desk")
            st.write("""
                Our AI Help Desk is a cutting-edge system designed to streamline your experience by providing quick and accurate responses to insurance-related queries.

                **Key Features:**
                * Intelligent query handling for insurance plans and claims.
                * Real-time information retrieval for accurate responses.
                * Seamless user experience with automated assistance.
                * AI-powered insights for better decision-making.

                Stay tuned for continuous improvements and updates to enhance your experience!
            """)

        elif page == "Claim Enquiry":
            st.write("## Claim Enquiry")
            st.write("Check the status of your submitted claims here.")

            if 'messages' not in st.session_state:
                st.session_state['messages'] = []

            for msg in st.session_state['messages']:
                if msg['sender'] == "AI":  # Only show AI responses
                    st.markdown(f"**{msg['sender']}**: {msg['text']}")

            user_input = st.text_input("Ask about your claim status:", key="user_input")
            if st.button("Send", key="send"):
                if user_input:
                    st.session_state['messages'].append({"sender": "User", "text": user_input})

                    ai_response = get_huggingface_response(user_input)

                    st.session_state['messages'].append({"sender": "AI", "text": ai_response})
                    st.rerun()  # Use st.rerun()

        elif page == "Inquiry Form":
            st.write("## Inquiry Form")
            st.write("Submit your inquiries using the form below.")
            st.text_input("Your Name", key="name")
            st.text_area("Your Inquiry", key="inquiry")
            st.button("Submit Inquiry", key="submit_inquiry") # Add functionality as needed

        if st.button("Logout", key="logout"):
            st.session_state['authenticated'] = False
            if 'current_page' in st.session_state:
                st.session_state.pop('current_page')
            if 'messages' in st.session_state:
                st.session_state.pop('messages')
            st.rerun()  # Use st.rerun()


if __name__ == "__main__":
    main()
