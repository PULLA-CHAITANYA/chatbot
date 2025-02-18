import streamlit as st
import time
import streamlit.components.v1 as components

# Authentication logic
def authenticate(username, password):
    return username == "admin" and password == "password123"

# Main application logic
def main():
    st.set_page_config(page_title="AI Dashboard", page_icon="🤖", layout="wide")
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        st.markdown("""
        <style>
        @keyframes slideIn {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        </style>
        <div class='slide-in'>
        """, unsafe_allow_html=True)
        
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to:", ["AI Chatbot", "Claim Status", "Dashboard", "Inquiry Form"])
        
        st.title(page)
        st.write(f"### Welcome to {page}!")
        st.text_area("Chat here:", "Hello! How can I assist you with {page}?")
        
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.rerun()

if __name__ == "__main__":
    main()
