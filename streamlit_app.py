import streamlit as st
import time
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import hashlib

# Load the distilBERT model and tokenizer from Hugging Face
model_name = "distilbert-base-uncased-distilled-squad"  # Using a popular pre-trained model for QA

# Use the slow tokenizer explicitly (set use_fast=False) to avoid errors
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Create a question-answering pipeline
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

# Streamlit authentication logic
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

# Streamlit app layout and interaction logic
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
                    st.session_state['current_page'] = "Home"  # Initialize current_page
                    st.success("Login successful!")
                    time.sleep(1)
                    st.experimental_rerun()
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
            st.experimental_rerun()

        st.title(page)
        st.write(f"### Welcome to {page}!")

        if page == "Home":
            # ... (Home page content - no changes needed)
            pass  # Placeholder, keep your existing Home page content here

        elif page == "Claim Enquiry":
            st.write("## Claim Enquiry")
            st.write("Check the status of your submitted claims here.")

            if 'messages' not in st.session_state:
                st.session_state['messages'] = []

            for msg in st.session_state['messages']:
                st.markdown(f"**{msg['sender']}**: {msg['text']}")

            user_input = st.text_input("Ask about your claim status:", key="user_input")
            if st.button("Send", key="send"):
                if user_input:
                    st.session_state['messages'].append({"sender": "User", "text": user_input})

                    # Simulate a claim status (replace with actual database/API call)
                    # Example statuses: "pending", "approved", "rejected"
                    claim_status = "pending"  # Replace with actual status retrieval

                    context = f"The claim status for your request is {claim_status}."

                    try:
                        result = qa_pipeline({'context': context, 'question': user_input})
                        ai_response = result['answer']
                    except Exception as e:  # Catch potential errors during QA
                        ai_response = f"Error processing your request: {e}"
                        st.error(ai_response) # Display the error in Streamlit

                    st.session_state['messages'].append({"sender": "AI", "text": ai_response})
                    st.experimental_rerun()  # Important: Rerun to update the chat display


        elif page == "Inquiry Form":
            # ... (Inquiry Form page content - no changes needed)
            pass # Placeholder, keep your existing Inquiry Form content here


        if st.button("Logout", key="logout"):
            st.session_state['authenticated'] = False
            if 'current_page' in st.session_state:  # Check if it exists before popping
                st.session_state.pop('current_page')
            if 'messages' in st.session_state: # Clear chat messages on logout
                st.session_state.pop('messages')
            st.experimental_rerun()

if __name__ == "__main__":
    main()
