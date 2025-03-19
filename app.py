import streamlit as st
import re
import string
import random
from zxcvbn import zxcvbn

def check_password_strength(password):
    result = zxcvbn(password)
    score = result['score']  # Score is between 0 (weak) and 4 (strong)
    feedback = result['feedback']
    
    strength_levels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    colors = ["#FF4B4B", "#FF9900", "#FFD700", "#9ACD32", "#008000"]
    return strength_levels[score], feedback, score, colors[score]

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    # Custom Styling
    st.markdown("""
        <style>
            .main-title {text-align: center; font-size: 32px; font-weight: bold; white-space: nowrap;}
            .sub-header {text-align: center; font-size: 20px !important;}
            .password-box {text-align: center;}
            .strength-box {font-size: 18px; font-weight: bold; padding: 10px; border-radius: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # Display the Title and sub-heading of the Application
    st.markdown("<h1 class='main-title'>🔐 Password Strength Checker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Enter a password to check its strength:</p>", unsafe_allow_html=True)
    
    # Password Requirements Section
    st.subheader("🔑 Password Guidelines")
    st.markdown("""
    <div style="padding: 10px; border-radius: 10px;">
        ✅ At least **8 characters** long<br>
        ✅ Includes **uppercase and lowercase** letters<br>
        ✅ Contains **numbers and special characters** (e.g., !@#$%^&*)<br>
        ✅ Avoids **common words** and easily guessable patterns<br>
        ✅ Is **unique** (not reused from other accounts)
    </div>
    """, unsafe_allow_html=True)
    
    # User input field for password
    password = st.text_input("Enter Password", type="password", key="password_input")
    
    if password:
        strength, feedback, score, color = check_password_strength(password) # Check password strength and display results
        
        st.markdown(f'<div class="strength-box" style="background-color:{color}; color: white; text-align: center;">{strength}</div>', unsafe_allow_html=True)
        st.progress((score + 1) / 5)  # Progress bar (normalized to 0-1)
        
        # Provide suggestions for improving password strength
        if feedback['suggestions']:
            st.write("💡 Suggestions to improve your password:")
            for suggestion in feedback['suggestions']:
                st.markdown(f"- {suggestion}")
        
        # Display warning messages if applicable
        if feedback['warning']:
            st.warning(feedback['warning'])
    
    # Password Generator Section
    st.subheader("🎲 Generate a Random Password")
    length = st.slider("Password Length", 8, 32, 12, step=1) # Slider to select password length
    generate_button = st.button("Generate Password") # Button to generate new password

    if generate_button:
        # Generate and display the password
        new_password = generate_password(length)
        st.text_input("Generated Password", new_password, key="generated_password_input", disabled=False)
        # Provide option to download the generated password
        st.download_button("Download Password", new_password, file_name="password.txt", mime="text/plain")

if __name__ == "__main__":main() # Running the application









