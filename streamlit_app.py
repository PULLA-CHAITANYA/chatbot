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
    .header {
        font-size: 24px;
        font-weight: bold;
        color: #FFEB3B;
    }
    /* ... (rest of your CSS styles) ... */
    </style>
    """, unsafe_allow_html=True)  # Include your CSS here

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.markdown("<div class='slide-in'>", unsafe_allow_html=True)  # Slide-in animation

        st.subheader("Sign In")
        with st.container():
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            if st.button("Login", key="login"):
                if authenticate(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['current_page'] = "AI Chatbot"
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("</div>", unsafe_allow_html=True)  # Close slide-in div

    else:
        st.sidebar.title("Navigation")

        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = "AI Chatbot"

        page = st.sidebar.radio("Go to:", ["AI Chatbot", "Claim Status", "Dashboard", "Inquiry Form"],
                               key="page_radio",
                               index=["AI Chatbot", "Claim Status", "Dashboard", "Inquiry Form"].index(st.session_state['current_page']))

        if page != st.session_state['current_page']:
            st.session_state['current_page'] = page
            st.rerun()

        st.title(page)
        st.write(f"### Welcome to {page}!")

        if page == "AI Chatbot":
            st.write("## AI Chatbot Details")
            st.write("This is the AI Chatbot page.  Here you can interact with our intelligent assistant.")
            st.text_area("Chat here:", "Hello! How can I assist you with the AI Chatbot?")
            # ... (Add chatbot interface here)
        elif page == "Claim Status":
            st.write("## Claim Status")
            st.write("Check the status of your submitted claims here.")
            # ... (Add claim status display)
        elif page == "Dashboard":
            st.write("## Dashboard")
            st.write("View key metrics and insights on this dashboard.")
            # ... (Add dashboard visualizations)
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
