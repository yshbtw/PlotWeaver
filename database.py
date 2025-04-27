from pymongo import MongoClient
from config import MONGODB_URI
import streamlit as st
import certifi
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
from datetime import datetime, timedelta
from config import RESEND_API_KEY
import resend

def get_database():
    try:
        client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=20000,
            retryWrites=True,
            w='majority'
        )
        
        client.admin.command('ping')
        return client['story_generator']
    except Exception as e:
        st.error(f"📝 Database connection failed: {str(e)}")
        return None

def is_valid_email(email):
    # RFC 5322 compliant email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def send_email(to_email, subject, body):
    if not RESEND_API_KEY:
        st.error("Email configuration is missing. Please set RESEND_API_KEY in .env file")
        return False
        
    try:
        resend.api_key = RESEND_API_KEY
        params = {
            "from": "PlotWeaver <onboarding@resend.dev>",
            "to": to_email,  # No need for list here
            "subject": subject,
            "text": body,  # Using plain text instead of HTML
        }
        
        response = resend.Emails.send(params)
        # Response is a dictionary containing email ID
        if response and isinstance(response, dict) and 'id' in response:
            return True
        st.error(f"Unexpected response from Resend: {response}")
        return False
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def generate_otp():
    return str(random.randint(100000, 999999))

# Initialize database and collections
db = get_database()
stories_collection = None
users_collection = None

if db is not None:
    stories_collection = db['stories']
    users_collection = db['users']

def create_user(username, password, email):
    if db is None:
        return False, "Database connection failed"
    
    if not is_valid_email(email):
        return False, "Invalid email format"
    
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    
    if users_collection.find_one({"email": email}):
        return False, "Email already exists"
    
    user = {
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }
    
    try:
        users_collection.insert_one(user)
        return True, "User created successfully"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    if db is None:
        return False, "Database connection failed"
    
    user = users_collection.find_one({"username": username})
    if not user:
        return False, "User not found"
    
    if check_password_hash(user['password'], password):
        return True, user
    return False, "Invalid password"

def delete_user(username):
    if db is None:
        return False, "Database connection failed"
    
    try:
        result = users_collection.delete_one({"username": username})
        if result.deleted_count > 0:
            return True, "User deleted successfully"
        return False, "User not found"
    except Exception as e:
        return False, str(e)

def store_otp(email, otp):
    if db is None:
        return False
    
    try:
        expiry = datetime.utcnow() + timedelta(minutes=10)  # OTP valid for 10 minutes
        users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "reset_otp": otp,
                    "otp_expiry": expiry
                }
            }
        )
        return True
    except Exception as e:
        st.error(f"Failed to store OTP: {str(e)}")
        return False

def verify_otp(email, otp):
    if db is None:
        return False, "Database connection failed"
    
    try:
        user = users_collection.find_one({
            "email": email,
            "reset_otp": otp,
            "otp_expiry": {"$gt": datetime.utcnow()}
        })
        
        if user:
            # Clear the OTP after successful verification
            users_collection.update_one(
                {"email": email},
                {"$unset": {"reset_otp": "", "otp_expiry": ""}}
            )
            return True, "OTP verified successfully"
        else:
            return False, "Invalid or expired OTP"
    except Exception as e:
        return False, str(e)

def initiate_password_reset(email):
    if db is None:
        return False, "Database connection failed"
    
    if not RESEND_API_KEY:
        return False, "Email service is not configured. Please contact administrator."
    
    user = users_collection.find_one({"email": email})
    if not user:
        return False, "No account found with this email"
    
    otp = generate_otp()
    if not store_otp(email, otp):
        return False, "Failed to generate reset code"
    
    email_body = f"""
    Hello {user.get('username', '')},
    
    You have requested to reset your password for your PlotWeaver account.
    Your OTP for password reset is: {otp}
    
    This OTP will expire in 10 minutes.
    
    If you did not request this password reset, please ignore this email.
    
    Best regards,
    PlotWeaver Team
    """
    
    if send_email(email, "Password Reset OTP - PlotWeaver", email_body):
        return True, "OTP sent to your email"
    return False, "Failed to send OTP email. Please check email configuration."

def reset_password_with_otp(email, otp, new_password):
    if db is None:
        return False, "Database connection failed"
    
    success, message = verify_otp(email, otp)
    if not success:
        return False, message
    
    try:
        users_collection.update_one(
            {"email": email},
            {"$set": {"password": generate_password_hash(new_password)}}
        )
        return True, "Password reset successful"
    except Exception as e:
        return False, str(e)

def find_user_by_email(email):
    if db is None:
        return None
    return users_collection.find_one({"email": email})