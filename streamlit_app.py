import streamlit as st
import time
import streamlit.components.v1 as components

# Authentication logic
def authenticate(username, password):
    return username == "admin" and password == "password123"

# Main application logic
def main():
    st.set_page_config(page_title="AI Dashboard", page_icon="🤖", layout="wide")
    
    # Add custom CSS for styling
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
    .subheader {
        font-size: 18px;
        color: #00E676;
        font-weight: bold;
    }
    .content {
        font-size: 16px;
        color: #B2FF59;
    }
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
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
    .login-box {
        padding: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }
    .button {
        background-color: #FF4081;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .sidebar {
        background-color: rgba(0, 0, 0, 0.7);
        color: #FFF;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        st.markdown("<div class='slide-in'>", unsafe_allow_html=True)
        
        st.subheader("Sign In")
        with st.container():
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            if st.button("Login", key="login"):
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
        page = st.sidebar.radio("Go to:", ["AI Chatbot", "Claim Status", "Dashboard", "Inquiry Form"], key="page", index=0)
        
        st.title(page)
        st.write(f"### Welcome to {page}!")
        st.text_area("Chat here:", f"Hello! How can I assist you with {page}?")

        if st.button("Logout", key="logout"):
            st.session_state['authenticated'] = False
            st.rerun()

if __name__ == "__main__":
    main()
