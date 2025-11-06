"""
Streamlit GUI for Digital Privacy Advisor Expert System.
Provides an interactive, conversational chat-based privacy assessment interface.

Run with: streamlit run app.py
"""

import streamlit as st
from typing import Dict, List, Any
from src.inference_engine import InferenceEngine


# Configure page
st.set_page_config(
    page_title="Digital Privacy Advisor",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stContainer {
        max-width: 900px;
        margin: 0 auto;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .high-priority {
        background-color: #ffe5e5;
        border-left: 4px solid #d32f2f;
    }
    .medium-priority {
        background-color: #fff8e5;
        border-left: 4px solid #f57c00;
    }
    .low-priority {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
    }
    .recommendation-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.75rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Initialize session state variables."""
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "assessment_complete" not in st.session_state:
        st.session_state.assessment_complete = False
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "risk_score" not in st.session_state:
        st.session_state.risk_score = 0


def get_questions() -> List[Dict[str, Any]]:
    """Get list of assessment questions."""
    return [
        {
            "key": "password_reuse",
            "question": "Do you reuse passwords across different accounts?",
            "type": "yes_no"
        },
        {
            "key": "password_manager",
            "question": "Do you use a password manager to store your passwords?",
            "type": "yes_no"
        },
        {
            "key": "two_factor",
            "question": "Do you have two-factor authentication (2FA) enabled on important accounts?",
            "type": "yes_no"
        },
        {
            "key": "public_wifi",
            "question": "Do you connect to public Wi-Fi networks (cafes, airports, etc.)?",
            "type": "yes_no"
        },
        {
            "key": "vpn",
            "question": "Do you use a VPN when accessing the internet?",
            "type": "yes_no"
        },
        {
            "key": "os_update",
            "question": "Do you keep your operating system and apps up to date?",
            "type": "yes_no"
        },
        {
            "key": "backup_data",
            "question": "Do you regularly back up your important data?",
            "type": "yes_no"
        },
        {
            "key": "email_encryption",
            "question": "Do you use email encryption for sensitive communications?",
            "type": "yes_no"
        },
        {
            "key": "app_permissions",
            "question": "List app permissions you grant (e.g., Location Contacts Camera Microphone)",
            "type": "multislot",
            "placeholder": "e.g., Location Contacts Camera or 'None'"
        },
        {
            "key": "social_media",
            "question": "List social media platforms you use (e.g., Facebook Instagram Twitter)",
            "type": "multislot",
            "placeholder": "e.g., Facebook Instagram Twitter or 'None'"
        }
    ]


def render_question(question: Dict[str, Any], question_num: int, total: int):
    """Render a single question in the UI."""
    st.markdown(f"### Question {question_num}/{total}")
    st.markdown(f"**{question['question']}**")
    
    key = question["key"]
    
    if question["type"] == "yes_no":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Yes", key=f"btn_yes_{key}", use_container_width=True):
                st.session_state.user_data[key] = "yes"
                st.session_state.current_question += 1
                st.rerun()
        with col2:
            if st.button("✗ No", key=f"btn_no_{key}", use_container_width=True):
                st.session_state.user_data[key] = "no"
                st.session_state.current_question += 1
                st.rerun()
    
    elif question["type"] == "multislot":
        user_input = st.text_input(
            label="Your answer",
            placeholder=question.get("placeholder", "Enter space-separated values"),
            key=f"input_{key}",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("→ Next", key=f"btn_next_{key}", use_container_width=True):
                if user_input.strip().lower() == "none" or user_input.strip() == "":
                    st.session_state.user_data[key] = []
                else:
                    st.session_state.user_data[key] = user_input.strip().split()
                st.session_state.current_question += 1
                st.rerun()
        with col2:
            if st.button("← Back", key=f"btn_back_{key}", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()


def display_results(recommendations: List[Dict[str, Any]], risk_score: int):
    """Display assessment results."""
    st.markdown("---")
    st.markdown("## 📋 Your Privacy Assessment Results")
    
    # Risk score
    risk_percentage = min(risk_score, 100)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label="Overall Risk Score", value=f"{risk_percentage}/100")
    
    # Categorize recommendations by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_recs = sorted(
        recommendations,
        key=lambda r: (priority_order.get(r["priority"], 3), -r["risk_score"])
    )
    
    high_priority = [r for r in sorted_recs if r["priority"] == "high"]
    medium_priority = [r for r in sorted_recs if r["priority"] == "medium"]
    low_priority = [r for r in sorted_recs if r["priority"] == "low"]
    
    # Display recommendations by priority
    if high_priority:
        st.markdown("### 🔴 HIGH PRIORITY — Address these immediately")
        for i, rec in enumerate(high_priority, 1):
            display_recommendation(rec, i, "high-priority")
    
    if medium_priority:
        st.markdown("### 🟡 MEDIUM PRIORITY — Consider these improvements")
        for i, rec in enumerate(medium_priority, 1):
            display_recommendation(rec, i, "medium-priority")
    
    if low_priority:
        st.markdown("### 🟢 LOW PRIORITY — Nice to have")
        for i, rec in enumerate(low_priority, 1):
            display_recommendation(rec, i, "low-priority")
    
    if not recommendations:
        st.success("Great! Based on your answers, you don't have immediate recommendations.")
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Start Over", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_data = {}
            st.session_state.assessment_complete = False
            st.session_state.recommendations = None
            st.session_state.risk_score = 0
            st.rerun()


def display_recommendation(rec: Dict[str, Any], index: int, priority_class: str):
    """Display a single recommendation in a styled box."""
    with st.container(border=True):
        st.markdown(f"**{index}. {rec['message']}**")
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Category: {rec['category']}")
        with col2:
            st.caption(f"Risk Score: +{rec['risk_score']}")
        st.write(f"**Details:** {rec['details']}")
        st.info(f"**📌 Action:** {rec['action']}")


def main():
    """Main Streamlit app."""
    initialize_session()
    
    # Sidebar mode selector
    with st.sidebar:
        st.markdown("## � Mode Selection")
        mode = st.radio(
            "Choose interaction mode:",
            ["Structured Assessment", "AI Chatbot"],
            help="Structured: Follow 10 questions | AI Chatbot: Ask free-form questions"
        )
    
    if mode == "Structured Assessment":
        run_structured_assessment()
    else:
        run_ai_chatbot()


def extract_relevant_rules(user_input: str) -> List[Dict[str, Any]]:
    """
    Extract relevant CLIPS rules based on user input keywords.
    Returns matching recommendations from the knowledge base.
    """
    user_input_lower = user_input.lower()
    
    # Define keyword-to-rule mappings
    rule_mappings = {
        # Password Security
        ("password", "reuse"): {
            "priority": "high",
            "category": "Password Security",
            "message": "Stop reusing passwords across accounts",
            "details": "Using the same password for multiple accounts means if one account is compromised, attackers can access all your accounts. This is one of the most common security mistakes.",
            "action": "Create unique passwords for each service immediately. Use a password manager to generate and store them.",
            "risk_score": 20,
            "rule": "password-reuse-rule"
        },
        ("password", "manager"): {
            "priority": "high",
            "category": "Password Security",
            "message": "Use a password manager",
            "details": "A password manager securely stores and encrypts all your passwords, allowing you to use strong, unique passwords for every account without memorizing them.",
            "action": "Install and set up a reputable password manager like Bitwarden (free), 1Password, or LastPass. Generate strong 16+ character passwords.",
            "risk_score": 15,
            "rule": "no-password-manager-rule"
        },
        ("2fa", "two-factor", "authentication", "2fa"): {
            "priority": "high",
            "category": "Account Security",
            "message": "Enable Two-Factor Authentication (2FA)",
            "details": "2FA requires a second verification method (authenticator app, security key) beyond your password. Even if someone has your password, they can't access your account without the second factor.",
            "action": "Enable 2FA using authenticator apps (Google Authenticator, Microsoft Authenticator, Authy) rather than SMS. Set it up for email, banking, and social media.",
            "risk_score": 20,
            "rule": "no-two-factor-rule"
        },
        ("vpn", "public wifi", "public wi-fi", "wifi security"): {
            "priority": "high",
            "category": "Network Security",
            "message": "Use VPN on public Wi-Fi networks",
            "details": "Public Wi-Fi at cafes, airports, and libraries is unencrypted. Attackers can intercept your data, steal passwords, and inject malware. A VPN encrypts all your traffic.",
            "action": "Install a trusted VPN service (Mullvad VPN, ProtonVPN, or NordVPN). Enable it before connecting to any public network.",
            "risk_score": 18,
            "rule": "public-wifi-no-vpn-rule"
        },
        ("vpn",): {
            "priority": "medium",
            "category": "Network Security",
            "message": "Consider using a VPN for all internet activity",
            "details": "A VPN hides your IP address and encrypts your traffic, protecting your privacy from ISPs, network administrators, and advertisers who track your online activity.",
            "action": "Research and subscribe to a reputable VPN service. Look for no-log policies, good speeds, and reviews from trusted sources.",
            "risk_score": 12,
            "rule": "no-vpn-rule"
        },
        ("update", "patch", "software", "security update"): {
            "priority": "high",
            "category": "Device Security",
            "message": "Keep your operating system and apps updated",
            "details": "Security updates patch known vulnerabilities that hackers actively exploit. Delaying updates leaves you exposed to known attacks that could compromise your entire device.",
            "action": "Enable automatic system updates in your OS settings. Manually check for app updates in your app store. Restart your device when prompted.",
            "risk_score": 15,
            "rule": "no-os-update-rule"
        },
        ("permission", "privacy settings", "app permission"): {
            "priority": "medium",
            "category": "Privacy Settings",
            "message": "Review and restrict app permissions",
            "details": "Many apps request unnecessary permissions like location, contacts, and camera. These permissions can be abused to track you or steal personal information.",
            "action": "Go to Settings → Privacy and revoke unnecessary permissions. Only grant permissions that are essential for app functionality. Disable location sharing by default.",
            "risk_score": 10,
            "rule": "excessive-permissions-rule"
        },
        ("social media", "facebook", "instagram", "twitter", "privacy settings"): {
            "priority": "medium",
            "category": "Social Media Privacy",
            "message": "Review privacy settings on social media",
            "details": "Social media platforms default to sharing too much information. Your data can be used for targeted ads, sold to third parties, or exploited for impersonation and social engineering.",
            "action": "Set profiles to private, disable location sharing, limit who can see your posts, review friend requests, disable tracking, and adjust targeted ad preferences.",
            "risk_score": 8,
            "rule": "many-social-media-rule"
        },
        ("backup", "data protection", "ransomware"): {
            "priority": "medium",
            "category": "Data Protection",
            "message": "Implement regular data backups",
            "details": "Backups protect against data loss from ransomware attacks, hardware failure, theft, or accidental deletion. Without backups, losing your device means losing irreplaceable files.",
            "action": "Set up automated backups using cloud services (Google Drive, OneDrive, iCloud) or external drives. Follow the 3-2-1 rule: 3 copies, 2 different media types, 1 offsite.",
            "risk_score": 10,
            "rule": "no-backup-rule"
        },
        ("email encryption", "encrypted email", "protonmail", "encryption"): {
            "priority": "low",
            "category": "Communication Security",
            "message": "Consider email encryption for sensitive communications",
            "details": "Regular emails are sent as plain text and can be intercepted. Encryption ensures only the recipient can read your sensitive messages.",
            "action": "For highly sensitive information, use ProtonMail or Tutanota for end-to-end encrypted email, or use PGP encryption with your current email provider.",
            "risk_score": 5,
            "rule": "no-email-encryption-rule"
        }
    }
    
    matched_rules = []
    
    for keywords, rule_data in rule_mappings.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                if rule_data not in matched_rules:
                    matched_rules.append(rule_data)
                break
    
    return matched_rules


def run_ai_chatbot():
    """Run the AI chatbot mode - searches CLIPS rules and provides explanations."""
    st.markdown("# 🤖 Digital Privacy Advisor Chatbot")
    st.markdown("*Ask me anything about digital privacy and security!*")
    st.markdown("💡 I search the expert system knowledge base to provide accurate, explainable answers.")
    
    # Initialize chat
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    
    # Display chat history
    for msg in st.session_state.chatbot_messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
    
    # User input
    user_input = st.chat_input("Ask about privacy or security (e.g., 'How to protect my password?')...")
    
    if user_input:
        # Add user message
        st.session_state.chatbot_messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Search through CLIPS rules
        matched_rules = extract_relevant_rules(user_input)
        
        with st.chat_message("assistant"):
            if matched_rules:
                # Display matched rules from knowledge base
                response_html = ""
                
                for i, rule in enumerate(matched_rules, 1):
                    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rule["priority"], "ℹ️")
                    
                    response_html += f"""
<div style="background-color: #f0f8ff; border-left: 4px solid #1f77b4; padding: 1.5rem; margin: 1rem 0; border-radius: 0.5rem;">
    <h3>{priority_icon} {rule['message']}</h3>
    
    <div style="background-color: #fff9e6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
        <strong>📚 From Knowledge Base - {rule['rule']}:</strong><br>
        {rule['details']}
    </div>
    
    <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
        <strong>✅ How to prevent/fix this:</strong><br>
        {rule['action']}
    </div>
    
    <div style="font-size: 0.9rem; color: #666;">
        <strong>Category:</strong> {rule['category']} | <strong>Risk Score:</strong> +{rule['risk_score']} | <strong>Priority:</strong> {rule['priority'].upper()}
    </div>
</div>
"""
                
                st.markdown(response_html, unsafe_allow_html=True)
                
                # Save the response
                assistant_response = f"Found {len(matched_rules)} matching rule(s) from knowledge base"
                st.session_state.chatbot_messages.append({"role": "assistant", "content": response_html})
            
            else:
                # If no rules matched, offer AI enrichment option
                response = """
<div style="background-color: #f0f8ff; border-left: 4px solid #1f77b4; padding: 1.5rem; margin: 1rem 0; border-radius: 0.5rem;">
    <strong>📋 No direct match in the knowledge base.</strong><br><br>
    Your question doesn't directly match our core privacy rules. Here are topics we cover:
    <ul>
        <li>🔐 <strong>Password Security:</strong> Password reuse, password managers</li>
        <li>🔑 <strong>Account Security:</strong> Two-factor authentication (2FA)</li>
        <li>🌐 <strong>Network Security:</strong> VPNs, public Wi-Fi safety</li>
        <li>💻 <strong>Device Security:</strong> Software updates, patches</li>
        <li>🎯 <strong>Privacy Settings:</strong> App permissions, location sharing</li>
        <li>📱 <strong>Social Media:</strong> Privacy settings, data exposure</li>
        <li>💾 <strong>Data Protection:</strong> Backups, ransomware protection</li>
        <li>✉️ <strong>Email Security:</strong> Email encryption</li>
    </ul>
    <strong>💡 Tip:</strong> Try asking about a specific topic above for detailed recommendations!
</div>
"""
                st.markdown(response, unsafe_allow_html=True)
                st.session_state.chatbot_messages.append({"role": "assistant", "content": response})


def run_structured_assessment():
    """Run the structured Q&A assessment mode."""
    
    # Assessment flow
    if not st.session_state.assessment_complete:
        questions = get_questions()
        total_questions = len(questions)
        
        # Progress bar
        progress = st.session_state.current_question / total_questions
        st.progress(progress)
        
        st.markdown("# 🔒 Privacy Assessment Quiz")
        st.markdown("*Answer 10 quick questions to assess your privacy posture*")
        
        if st.session_state.current_question < total_questions:
            # Display current question
            question = questions[st.session_state.current_question]
            render_question(question, st.session_state.current_question + 1, total_questions)
            
            # Back button for first question
            if st.session_state.current_question > 0:
                if st.button("← Previous Question"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        else:
            # All questions answered — run inference and show results
            engine = InferenceEngine()
            recommendations, risk_score = engine.process(st.session_state.user_data)
            st.session_state.recommendations = recommendations
            st.session_state.risk_score = risk_score
            st.session_state.assessment_complete = True
            st.rerun()
    
    else:
        # Show results
        if st.session_state.recommendations is not None:
            display_results(st.session_state.recommendations, st.session_state.risk_score)


if __name__ == "__main__":
    main()
