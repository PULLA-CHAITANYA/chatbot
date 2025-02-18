import streamlit as st
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import hashlib
import time

# Load ALBERT model and tokenizer from Hugging Face
model_name = "Chaithu93839/my-ai-help-desk"  # Replace with your model on Hugging Face

# Use the slow tokenizer explicitly
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Create a question answering pipeline
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

# Placeholder for user data (replace with a database or secure storage)
users = {}

def simple_hash(password):  # Simple hashing function (INSECURE - for demo only)
    return hashlib.sha256(password.encode()).hexdigest()

# Hash the default password (do this offline and store the hash)
default_password = "password123"
default_password_hash = simple_hash(default_password)
users["admin"] = default_password_hash

def authenticate(username, password):
    if username in users:
        stored_hash = users[username]
        entered_hash = simple_hash(password)
        return stored_hash == entered_hash
    return False

def main():
    # Streamlit Page Configuration
    st.set_page_config(page_title="AI Help Desk", page_icon="🤖", layout="wide")

    # Check for authentication status
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Handle login if not authenticated
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
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    # If authenticated, show the main app with pages
    if st.session_state['authenticated']:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to:", ["Home", "Inquiry Form", "Claim Enquiry"])

        # Handle page navigation
        if page == "Home":
            st.title("Welcome to AI Help Desk")
            st.write("""
                Welcome to the AI Help Desk! Here, you can ask questions related to your insurance plans, claims, and more.
            """)

        elif page == "Inquiry Form":
            st.title("Submit Your Inquiry")
            st.write("""
                If you have any questions, feel free to ask below. Our AI Help Desk will provide quick and accurate responses.
            """)

            # Create a form to capture user inquiry (question)
            question = st.text_input("Ask a question about insurance or claims:")

            if question:
                # Get the model's response
                answer = qa_pipeline({
                    'context': "This is a placeholder context. Replace with relevant context from your insurance data.",
                    'question': question
                })
                st.write(f"**Answer:** {answer['answer']}")

        elif page == "Claim Enquiry":
            st.title("Claim Enquiry")
            st.write("""
                Check the status of your submitted claims here.
            """)
            
            # Chat interface for checking claim status
            if 'messages' not in st.session_state:
                st.session_state['messages'] = []

            # Display chat messages
            for msg in st.session_state['messages']:
                st.markdown(f"**{msg['sender']}**: {msg['text']}")

            # Input and button for sending messages
            user_input = st.text_input("Ask about your claim status:", key="user_input")
            if st.button("Send", key="send"):
                if user_input:
                    # Simulate user input
                    st.session_state['messages'].append({"sender": "User", "text": user_input})

                    # Get AI response using the pipeline
                    answer = qa_pipeline({
                        'context': "This is a placeholder context for claim status. Replace with real data.",
                        'question': user_input
                    })
                    st.session_state['messages'].append({"sender": "AI", "text": answer['answer']})
                    st.experimental_rerun()

        # Optional: Add a logout button
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state.pop('current_page', None)
            st.rerun()

if __name__ == "__main__":
    main()
