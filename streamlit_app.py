import os
import streamlit as st
import time
import hashlib
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from safetensors import safe_open

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

# Define the path to the model directory
model_path = "C:/Users/chait/OneDrive/Desktop/Hackathon/GenFormat/results/checkpoint_5"

# Check if safetensors file exists
safetensors_file = os.path.join(model_path, "model.safetensors")
if os.path.exists(safetensors_file):
    print("Loading model from safetensors file...")
    # Open safetensors file
    with safe_open(safetensors_file, framework="pt") as f:
        model_weights = {key: f.get_tensor(key) for key in f.keys()}
        
    # Load model and assign the weights
    model = AutoModelForQuestionAnswering.from_pretrained(model_path, config=model_path)
    model.load_state_dict(model_weights)
    print("Model loaded successfully with safetensors weights.")
else:
    print("No safetensors file found. Please ensure the model is correctly placed.")
    # Fallback for loading a regular pytorch model
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Create the Question Answering pipeline
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

def main():
    st.set_page_config(page_title="AI Dashboard", page_icon="🤖", layout="wide")

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
                    st.rerun()
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
            st.rerun()

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
            
            # Chat interface
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

                    # Get AI response using Question Answering model
                    context = "The insurance claim process includes several steps including verification, approval, and disbursement."  # Replace with your actual context data
                    result = qa_pipeline(question=user_input, context=context)
                    ai_response = result['answer']
                    st.session_state['messages'].append({"sender": "AI", "text": ai_response})
                    st.experimental_rerun()

        elif page == "Inquiry Form":
            st.write("## Inquiry Form")
            st.write("Submit your inquiries using the form below.")
            # ... (Add inquiry form elements)

        if st.button("Logout", key="logout"):
            st.session_state['authenticated'] = False
            st.session_state.pop('current_page')
            st.rerun()

if __name__ == "__main__":
    main()
