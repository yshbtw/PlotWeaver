import streamlit as st
from database import (
    create_user, verify_user, delete_user, 
    initiate_password_reset, reset_password_with_otp,
    find_user_by_email, is_valid_email
)

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'reset_password_mode' not in st.session_state:
        st.session_state.reset_password_mode = False
    if 'reset_email' not in st.session_state:
        st.session_state.reset_email = None
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False

def login_ui():
    st.markdown("### 🔐 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2, col3 = st.columns([1, 1.5, 2])
    with col1:
        if st.button("Login"):
            if username and password:
                success, result = verify_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please fill in all fields")
    
    with col2:
        if st.button("Forgot Password?"):
            st.session_state.reset_password_mode = True
            st.session_state.otp_sent = False
            st.session_state.reset_email = None
            st.rerun()

def reset_password_ui():
    st.markdown("### 🔑 Reset Password")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Back to Login"):
            st.session_state.reset_password_mode = False
            st.session_state.otp_sent = False
            st.session_state.reset_email = None
            st.rerun()
    
    if not st.session_state.otp_sent:
        email = st.text_input("Enter your email")
        if email and not is_valid_email(email):
            st.error("Please enter a valid email address")
        
        if st.button("Send OTP"):
            if email and is_valid_email(email):
                success, message = initiate_password_reset(email)
                if success:
                    st.session_state.otp_sent = True
                    st.session_state.reset_email = email
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter a valid email address")
    
    else:
        st.info(f"OTP has been sent to {st.session_state.reset_email}")
        otp = st.text_input("Enter OTP", max_chars=6)
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        col1, col2 = st.columns([1.5, 3])
        with col1:
            if st.button("Reset Password"):
                if otp and new_password and confirm_password:
                    if new_password == confirm_password:
                        success, message = reset_password_with_otp(
                            st.session_state.reset_email,
                            otp,
                            new_password
                        )
                        if success:
                            st.success(message)
                            st.session_state.reset_password_mode = False
                            st.session_state.otp_sent = False
                            st.session_state.reset_email = None
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
            
            if st.button("Resend OTP"):
                success, message = initiate_password_reset(st.session_state.reset_email)
                if success:
                    st.success("New OTP sent to your email")
                else:
                    st.error(message)

def signup_ui():
    st.markdown("### 📝 Sign Up")
    username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Sign Up"):
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = create_user(username, password, email)
                    if success:
                        st.success(message)
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def user_profile_ui():
    st.markdown(f"### 👤 Welcome, {st.session_state.username}!")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        if st.button("Delete Account", type="primary"):
            if st.session_state.username:
                success, message = delete_user(st.session_state.username)
                if success:
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def auth_ui():
    init_session_state()
    
    if not st.session_state.logged_in:
        if st.session_state.reset_password_mode:
            reset_password_ui()
            return False
        else:
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            with tab1:
                login_ui()
            with tab2:
                signup_ui()
            return False
    else:
        user_profile_ui()
        return True
