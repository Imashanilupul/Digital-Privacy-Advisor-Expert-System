"""
AI Chatbot for Digital Privacy Advisor using Google Gemini API.
Provides an interactive conversational interface where users can ask free-form questions
about digital privacy and security, with intelligent responses powered by Gemini.
"""

import streamlit as st
import google.generativeai as genai
from typing import Optional


# Configure page
st.set_page_config(
    page_title="Privacy Advisor Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: flex;
        gap: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
        justify-content: flex-end;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #7b1fa2;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #d32f2f;
    }
    .info-box {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


SYSTEM_PROMPT = """You are the Digital Privacy Advisor chatbot, an expert system specializing in digital privacy and security.

Your knowledge base covers:
1. **Password Security**: Password reuse risks, password managers, strong password practices
2. **Account Security**: Two-factor authentication (2FA), account recovery, backup codes
3. **Network Security**: VPNs, public Wi-Fi risks, encrypted connections, DNS privacy
4. **Device Security**: Operating system updates, app updates, antivirus, firewalls
5. **Privacy Settings**: App permissions, location tracking, data collection, privacy controls
6. **Social Media Privacy**: Profile privacy, friend lists, sharing settings, data exposure
7. **Data Protection**: Backups, encryption, ransomware protection, data loss prevention
8. **Communication Security**: Email encryption, encrypted messaging, PGP, secure chat apps

When users ask questions:
- Provide clear, actionable advice
- Explain WHY security practices matter
- Offer specific tools/services when relevant (e.g., Bitwarden for password managers, ProtonVPN for VPN)
- Assess risk levels (High/Medium/Low) when appropriate
- Recommend immediate actions vs. nice-to-have improvements
- Be friendly and non-judgmental
- Ask clarifying questions if needed

Always prioritize user privacy and security. If asked about non-privacy topics, politely redirect to privacy/security topics."""


def initialize_session():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "model" not in st.session_state:
        st.session_state.model = None


def configure_gemini(api_key: str) -> Optional[object]:
    """Configure and return Gemini model instance."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        return model
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        return None


def get_chatbot_response(model: object, user_message: str) -> str:
    """Get response from Gemini chatbot."""
    try:
        # Prepare conversation history for context
        chat_history = []
        for msg in st.session_state.messages[-6:]:  # Last 3 exchanges (6 messages)
            if msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            else:
                chat_history.append({"role": "model", "parts": [msg["content"]]})
        
        # Start a new chat session
        chat = model.start_chat(history=chat_history)
        
        # Get response
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"


def display_chat_history():
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Privacy Advisor:** {message['content']}")


def main():
    """Main chatbot interface."""
    initialize_session()
    
    # Header
    st.markdown("# 🤖 Digital Privacy Advisor Chatbot")
    st.markdown("*Ask me anything about digital privacy and security!*")
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("### Google Gemini API Setup")
        
        api_key_input = st.text_input(
            "AIzaSyCF8cqv3LIiQC3tmwpNg59FO1Ascet1DVk",
            type="password",
            help="Get your API key from https://aistudio.google.com/app/apikey"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.model = configure_gemini(api_key_input)
            if st.session_state.model:
                st.success("✓ Gemini API configured successfully!")
        
        st.markdown("---")
        
        if st.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About this Chatbot")
        st.info(
            """This chatbot uses Google's Gemini AI to answer questions about digital privacy and security.
            
It covers:
- 🔐 Password security
- 🔑 Account security & 2FA
- 🌐 Network security & VPNs
- 💾 Device security & updates
- 👁️ Privacy settings
- 📱 Social media privacy
- 💿 Data protection & backups
- 📧 Communication security"""
        )
    
    # Main chat area
    if not st.session_state.api_key or not st.session_state.model:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to start chatting.")
        st.markdown(
            """
### Getting Started
1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Paste your API key in the sidebar
3. Start asking questions about privacy and security!
            """
        )
        return
    
    # Display chat history
    st.markdown("---")
    display_chat_history()
    st.markdown("---")
    
    # User input
    user_input = st.text_input(
        "Ask a question about digital privacy or security:",
        placeholder="e.g., Should I use a VPN? How do I enable 2FA? What's a good password manager?"
    )
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get chatbot response
        with st.spinner("🤔 Thinking..."):
            response = get_chatbot_response(st.session_state.model, user_input)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    # Quick action buttons
    if len(st.session_state.messages) == 0:
        st.markdown("### 💡 Try asking about:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔐 Password Security", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What are the best practices for password security?"
                })
                st.rerun()
        
        with col2:
            if st.button("🌐 VPN & Networks", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Should I use a VPN and what are the benefits?"
                })
                st.rerun()
        
        with col3:
            if st.button("🔑 2FA & Accounts", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "How do I set up two-factor authentication and why is it important?"
                })
                st.rerun()


if __name__ == "__main__":
    main()
