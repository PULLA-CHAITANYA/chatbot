import streamlit as st
import time
import hashlib

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

        page = st.sidebar.radio("Go to:", ["Home", "Claim Status", "Inquiry Form"],
                               key="page_radio",
                               index=["Home", "Claim Status", "Inquiry Form"].index(st.session_state['current_page']))

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
        elif page == "Claim Status":
            st.write("## Claim Status")
            st.write("Check the status of your submitted claims here.")
            # ... (Add claim status display)
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
