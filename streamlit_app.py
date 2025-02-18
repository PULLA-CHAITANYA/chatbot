import streamlit as st
import time

# Function to simulate a splash screen with animation
def splash_screen():
    st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    </style>
    <div class='centered'>
        <h2>🔄 Loading AI Dashboard...</h2>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state['splash_shown'] = True

# Authentication logic
def authenticate(username, password):
    return username == "admin" and password == "password123"

# Main application logic
def main():
    st.set_page_config(page_title="AI Dashboard", page_icon="🤖", layout="wide")
    
    if 'splash_shown' not in st.session_state:
        splash_screen()
        st.experimental_rerun()

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.success("Login successful!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to:", ["AI Chatbot", "Claim Status", "Dashboard", "Inquiry Form"])
        
        st.title(page)
        st.write(f"### Welcome to {page}!")
        st.text_area("Chat here:", "Hello! How can I assist you with {page}?")
        
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
