"""
Streamlit GUI for Digital Privacy Advisor Expert System.
Provides an interactive, conversational chat-based privacy assessment interface.

Run with: streamlit run app.py
"""

import streamlit as st
from typing import Dict, List, Any
from src.inference_engine import InferenceEngine
from src.issue_classifier import IssueClassifier
import google.generativeai as genai


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
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "assessment_complete" not in st.session_state:
        st.session_state.assessment_complete = False
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "risk_score" not in st.session_state:
        st.session_state.risk_score = 0
    # Issue-based assessment variables
    if "user_issue" not in st.session_state:
        st.session_state.user_issue = None
    if "issue_classified" not in st.session_state:
        st.session_state.issue_classified = False
    if "issue_classification" not in st.session_state:
        st.session_state.issue_classification = None
    if "followup_questions" not in st.session_state:
        st.session_state.followup_questions = []
    if "followup_answers" not in st.session_state:
        st.session_state.followup_answers = {}
    if "report_generated" not in st.session_state:
        st.session_state.report_generated = False
    if "final_report" not in st.session_state:
        st.session_state.final_report = None


def get_all_questions() -> Dict[str, Dict[str, Any]]:
    """Get all available assessment questions organized by category."""
    return {
        # Password Security Questions
        "password_reuse": {
            "category": "Password Security",
            "question": "Do you reuse passwords across different accounts?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["password_manager_importance", "password_strength"],
                "no": ["password_manager"]
            }
        },
        "password_manager": {
            "category": "Password Security",
            "question": "Do you use a password manager to store your passwords?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["password_reuse_avoided"],
                "no": ["password_manager_importance"]
            }
        },
        "password_manager_importance": {
            "category": "Password Security",
            "question": "Are you aware that password managers can help you create unique passwords?",
            "type": "yes_no",
            "depends_on": ["password_reuse", "password_manager"],
            "condition": lambda data: data.get("password_reuse") == "yes" or data.get("password_manager") == "no",
            "follow_ups": {"yes": [], "no": []}
        },
        "password_strength": {
            "category": "Password Security",
            "question": "Do you create strong passwords (mix of uppercase, lowercase, numbers, symbols)?",
            "type": "yes_no",
            "depends_on": ["password_reuse"],
            "condition": lambda data: data.get("password_reuse") == "yes",
            "follow_ups": {"yes": [], "no": []}
        },
        "password_reuse_avoided": {
            "category": "Password Security",
            "question": "How do you remember your unique passwords without a manager?",
            "type": "text",
            "depends_on": ["password_manager"],
            "condition": lambda data: data.get("password_manager") == "yes",
            "follow_ups": {}
        },
        
        # Account Security Questions
        "two_factor": {
            "category": "Account Security",
            "question": "Do you have two-factor authentication (2FA) enabled on important accounts?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["two_factor_method"],
                "no": ["two_factor_barriers"]
            }
        },
        "two_factor_method": {
            "category": "Account Security",
            "question": "What method do you use for 2FA?",
            "type": "choice",
            "options": ["Authenticator App (Google/Authy)", "SMS", "Biometric", "Multiple Methods"],
            "depends_on": ["two_factor"],
            "condition": lambda data: data.get("two_factor") == "yes",
            "follow_ups": {}
        },
        "two_factor_barriers": {
            "category": "Account Security",
            "question": "What's preventing you from using 2FA?",
            "type": "choice",
            "options": ["Not aware of it", "Too complicated", "Concerned about access", "Don't need it"],
            "depends_on": ["two_factor"],
            "condition": lambda data: data.get("two_factor") == "no",
            "follow_ups": {}
        },
        
        # Network Security Questions
        "public_wifi": {
            "category": "Network Security",
            "question": "Do you connect to public Wi-Fi networks (cafes, airports, etc.)?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["vpn", "public_wifi_behavior"],
                "no": ["vpn_usage"]
            }
        },
        "public_wifi_behavior": {
            "category": "Network Security",
            "question": "What do you do on public Wi-Fi? (Banking, emails, social media, etc.)",
            "type": "text",
            "depends_on": ["public_wifi"],
            "condition": lambda data: data.get("public_wifi") == "yes",
            "follow_ups": {}
        },
        "vpn": {
            "category": "Network Security",
            "question": "Do you use a VPN when accessing the internet?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["vpn_frequency"],
                "no": ["vpn_reason"]
            }
        },
        "vpn_frequency": {
            "category": "Network Security",
            "question": "How often do you use a VPN?",
            "type": "choice",
            "options": ["Always", "On public Wi-Fi only", "Sometimes", "Rarely"],
            "depends_on": ["vpn"],
            "condition": lambda data: data.get("vpn") == "yes",
            "follow_ups": {}
        },
        "vpn_reason": {
            "category": "Network Security",
            "question": "Why don't you use a VPN?",
            "type": "choice",
            "options": ["Not aware of it", "Too slow", "Too expensive", "Don't think I need it"],
            "depends_on": ["vpn"],
            "condition": lambda data: data.get("vpn") == "no",
            "follow_ups": {}
        },
        "vpn_usage": {
            "category": "Network Security",
            "question": "Do you use a VPN for general internet privacy?",
            "type": "yes_no",
            "depends_on": ["public_wifi"],
            "condition": lambda data: data.get("public_wifi") == "no",
            "follow_ups": {"yes": [], "no": []}
        },
        
        # Device Security Questions
        "os_update": {
            "category": "Device Security",
            "question": "Do you keep your operating system and apps up to date?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["auto_update"],
                "no": ["update_barriers"]
            }
        },
        "auto_update": {
            "category": "Device Security",
            "question": "Do you have automatic updates enabled?",
            "type": "yes_no",
            "depends_on": ["os_update"],
            "condition": lambda data: data.get("os_update") == "yes",
            "follow_ups": {}
        },
        "update_barriers": {
            "category": "Device Security",
            "question": "What prevents you from updating regularly?",
            "type": "choice",
            "options": ["Forget", "Takes too long", "Causes issues", "Don't see the need"],
            "depends_on": ["os_update"],
            "condition": lambda data: data.get("os_update") == "no",
            "follow_ups": {}
        },
        "antivirus": {
            "category": "Device Security",
            "question": "Do you use antivirus/anti-malware software?",
            "type": "yes_no",
            "depends_on": ["os_update"],
            "condition": lambda data: True,
            "follow_ups": {"yes": [], "no": []}
        },
        
        # Data Protection Questions
        "backup_data": {
            "category": "Data Protection",
            "question": "Do you regularly back up your important data?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["backup_method", "backup_encryption"],
                "no": ["backup_reasons"]
            }
        },
        "backup_method": {
            "category": "Data Protection",
            "question": "Where do you back up your data?",
            "type": "choice",
            "options": ["Cloud (Google Drive, OneDrive)", "External Drive", "Both", "Other"],
            "depends_on": ["backup_data"],
            "condition": lambda data: data.get("backup_data") == "yes",
            "follow_ups": {}
        },
        "backup_encryption": {
            "category": "Data Protection",
            "question": "Is your backup encrypted?",
            "type": "yes_no",
            "depends_on": ["backup_data"],
            "condition": lambda data: data.get("backup_data") == "yes",
            "follow_ups": {}
        },
        "backup_reasons": {
            "category": "Data Protection",
            "question": "Why don't you back up data?",
            "type": "choice",
            "options": ["Don't have important data", "Too complicated", "Storage costs", "Never thought about it"],
            "depends_on": ["backup_data"],
            "condition": lambda data: data.get("backup_data") == "no",
            "follow_ups": {}
        },
        
        # Communication Security Questions
        "email_encryption": {
            "category": "Communication Security",
            "question": "Do you use email encryption for sensitive communications?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["email_service"],
                "no": ["email_sensitivity"]
            }
        },
        "email_service": {
            "category": "Communication Security",
            "question": "Which encrypted email service do you use?",
            "type": "text",
            "depends_on": ["email_encryption"],
            "condition": lambda data: data.get("email_encryption") == "yes",
            "follow_ups": {}
        },
        "email_sensitivity": {
            "category": "Communication Security",
            "question": "Do you send sensitive information via email?",
            "type": "yes_no",
            "depends_on": ["email_encryption"],
            "condition": lambda data: data.get("email_encryption") == "no",
            "follow_ups": {}
        },
        
        # Privacy Settings Questions
        "privacy_settings": {
            "category": "Privacy Settings",
            "question": "Do you regularly review app permissions on your devices?",
            "type": "yes_no",
            "depends_on": None,
            "follow_ups": {
                "yes": ["permission_management"],
                "no": ["permission_concerns"]
            }
        },
        "permission_management": {
            "category": "Privacy Settings",
            "question": "How many apps have access to your camera/microphone?",
            "type": "choice",
            "options": ["None", "Few", "Many", "Don't know"],
            "depends_on": ["privacy_settings"],
            "condition": lambda data: data.get("privacy_settings") == "yes",
            "follow_ups": {}
        },
        "permission_concerns": {
            "category": "Privacy Settings",
            "question": "Are you concerned about app permissions?",
            "type": "yes_no",
            "depends_on": ["privacy_settings"],
            "condition": lambda data: data.get("privacy_settings") == "no",
            "follow_ups": {}
        },
        
        # Social Media Questions
        "social_media_usage": {
            "category": "Social Media",
            "question": "How active are you on social media?",
            "type": "choice",
            "options": ["Very Active", "Moderately Active", "Rarely", "Don't use it"],
            "depends_on": None,
            "follow_ups": {
                "Very Active": ["social_media_privacy"],
                "Moderately Active": ["social_media_privacy"],
                "Rarely": [],
                "Don't use it": []
            }
        },
        "social_media_privacy": {
            "category": "Social Media",
            "question": "How private are your social media accounts?",
            "type": "choice",
            "options": ["Public", "Friends only", "Private", "Don't share personal info"],
            "depends_on": ["social_media_usage"],
            "condition": lambda data: data.get("social_media_usage") in ["Very Active", "Moderately Active"],
            "follow_ups": {}
        },
    }


def get_next_questions(user_data: Dict[str, Any]) -> List[str]:
    """
    Intelligently determine the next questions based on previous answers.
    Uses adaptive branching to customize the assessment.
    """
    all_questions = get_all_questions()
    asked_questions = set(user_data.keys())
    next_questions = []
    
    # Start with initial questions if none answered yet
    if not asked_questions:
        return [
            "password_reuse",
            "two_factor",
            "public_wifi",
            "os_update",
            "backup_data",
            "email_encryption",
            "privacy_settings",
            "social_media_usage",
            "antivirus"
        ]
    
    # Determine follow-up questions based on latest answer
    last_answered_key = list(user_data.keys())[-1] if user_data else None
    
    if last_answered_key in all_questions:
        question_info = all_questions[last_answered_key]
        last_answer = user_data[last_answered_key]
        
        # Get follow-up questions based on answer
        if "follow_ups" in question_info and last_answer in question_info["follow_ups"]:
            follow_ups = question_info["follow_ups"][last_answer]
            for follow_up_key in follow_ups:
                if follow_up_key not in asked_questions:
                    next_questions.append(follow_up_key)
    
    # Check for conditional questions
    for q_key, q_info in all_questions.items():
        if q_key not in asked_questions:
            depends_on = q_info.get("depends_on")
            condition_func = q_info.get("condition")
            
            # Check if dependencies are met
            if depends_on is None or all(dep in asked_questions for dep in (depends_on if isinstance(depends_on, list) else [depends_on])):
                # Check conditional logic
                if condition_func is None or condition_func(user_data):
                    if q_key not in next_questions:
                        next_questions.append(q_key)
    
    return next_questions[:1] if next_questions else []  # Return one question at a time


def get_questions() -> List[Dict[str, Any]]:
    """
    Get dynamically adapted questions for the current assessment state.
    """
    all_questions = get_all_questions()
    user_data = st.session_state.user_data
    next_q_keys = get_next_questions(user_data)
    
    questions = []
    for key in next_q_keys:
        if key in all_questions:
            q = all_questions[key].copy()
            q["key"] = key
            questions.append(q)
    
    return questions


def render_question(question: Dict[str, Any], question_num: int, total: int):
    """Render a single question in the UI with adaptive behavior."""
    st.markdown(f"### Question {question_num}/{total}")
    st.markdown(f"**{question['question']}**")
    
    # Show category
    if "category" in question:
        st.caption(f"📁 Category: {question['category']}")
    
    key = question["key"]
    
    if question["type"] == "yes_no":
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Yes", key=f"btn_yes_{key}", use_container_width=True):
                st.session_state.user_data[key] = "yes"
                st.rerun()
        with col2:
            if st.button("❌ No", key=f"btn_no_{key}", use_container_width=True):
                st.session_state.user_data[key] = "no"
                st.rerun()
    
    elif question["type"] == "choice":
        options = question.get("options", [])
        selected = st.radio(
            label="Select one:",
            options=options,
            key=f"radio_{key}",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("→ Confirm", key=f"btn_confirm_{key}", use_container_width=True):
                st.session_state.user_data[key] = selected
                st.rerun()
    
    elif question["type"] == "text":
        user_input = st.text_input(
            label="Your answer:",
            placeholder="Enter your response",
            key=f"input_{key}",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("→ Next", key=f"btn_next_{key}", use_container_width=True):
                if user_input.strip():
                    st.session_state.user_data[key] = user_input.strip()
                    st.rerun()
                else:
                    st.warning("Please enter a response")
    
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
        if st.button("🔄 Start Over", use_container_width=True):
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
    
    # Sidebar for API key
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Gemini API Key:",
            type="password",
            help="Get from https://aistudio.google.com/app/apikey"
        )
        if api_key:
            st.success("✓ API key configured")
    
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to use the Privacy Advisor")
        st.markdown("""
## Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy and paste it in the sidebar
4. Start analyzing your privacy concerns
        """)
        return
    
    # Run issue-based assessment
    run_issue_based_assessment(api_key)


def run_issue_based_assessment(api_key: str):
    """Run AI-powered issue classification and detailed analysis."""
    
    st.markdown("# 🔒 Digital Privacy Advisor - Expert System")
    st.markdown("*Explain your privacy concern, and we'll analyze it with AI*")
    
    # Step 1: Get user issue description
    if not st.session_state.user_issue:
        st.markdown("## Step 1️⃣ Describe Your Privacy Concern")
        st.info("💡 Be specific about what worries you. Examples: 'I reuse passwords everywhere', 'I'm concerned about public WiFi'")
        
        user_issue = st.text_area(
            "What is your privacy or security concern?",
            placeholder="Describe your issue in detail...",
            height=150,
            key="issue_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            pass
        with col2:
            if st.button("🔍 Analyze", use_container_width=True):
                if user_issue.strip():
                    st.session_state.user_issue = user_issue
                    st.rerun()
                else:
                    st.warning("Please describe your concern")
        return
    
    # Step 2: Classify the issue
    if not st.session_state.issue_classified:
        st.markdown("## Step 2️⃣ Analyzing Your Concern")
        
        with st.spinner("🤖 Using AI to analyze your privacy concern..."):
            try:
                classifier = IssueClassifier(api_key)
                classification = classifier.classify_issue(st.session_state.user_issue)
                st.session_state.issue_classification = classification
                
                # Generate follow-up questions
                followup_questions = classifier.generate_followup_questions(classification)
                st.session_state.followup_questions = followup_questions
                st.session_state.issue_classified = True
                
            except Exception as e:
                st.error(f"Error analyzing issue: {e}")
                if st.button("🔄 Try Again"):
                    st.session_state.user_issue = None
                    st.session_state.issue_classified = False
                return
        
        st.rerun()
    
    # Step 3: Display classification and collect follow-up answers
    if st.session_state.issue_classified and not st.session_state.report_generated:
        classification = st.session_state.issue_classification
        classifier = IssueClassifier(api_key)
        
        # Display analysis
        st.markdown("## Step 2️⃣ Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            category = classification.get("primary_category", "general")
            icon = classifier.get_category_icon(category)
            st.markdown(f"### {icon} Category")
            st.markdown(f"**{category.replace('_', ' ').title()}**")
        
        with col2:
            severity = classification.get("severity", "medium").upper()
            severity_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "🔴🔴"}
            st.markdown(f"### Severity")
            st.markdown(f"{severity_icon.get(severity, '🔴')} **{severity}**")
        
        with col3:
            risk = classification.get("risk_level", 50)
            st.markdown(f"### Risk Level")
            st.markdown(f"**{risk}/100**")
        
        st.divider()
        
        # Display summary and concerns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📋 Summary:**")
            st.write(classification.get("summary", "Issue identified"))
        
        with col2:
            st.markdown("**⚠️ Key Concerns:**")
            for concern in classification.get("key_concerns", []):
                st.write(f"• {concern}")
        
        st.divider()
        
        # Follow-up questions
        st.markdown("## Step 3️⃣ Answer Follow-Up Questions")
        st.info("These questions help us understand your situation better and provide targeted recommendations")
        
        followup_questions = st.session_state.followup_questions
        all_answered = True
        
        for i, question in enumerate(followup_questions, 1):
            st.markdown(f"### Q{i}: {question['question']}")
            st.caption(f"💡 {question.get('context', '')}")
            
            q_id = question["id"]
            q_type = question.get("type", "text")
            
            if q_type == "yes_no":
                answer = st.radio(
                    label="Select one:",
                    options=["Yes", "No"],
                    key=f"followup_{q_id}",
                    label_visibility="collapsed"
                )
                st.session_state.followup_answers[q_id] = answer
            
            elif q_type == "choice":
                options = question.get("options", [])
                answer = st.selectbox(
                    label="Select one:",
                    options=options,
                    key=f"followup_{q_id}",
                    label_visibility="collapsed"
                )
                st.session_state.followup_answers[q_id] = answer
            
            elif q_type == "text":
                answer = st.text_input(
                    label="Your answer:",
                    key=f"followup_{q_id}",
                    label_visibility="collapsed"
                )
                if answer:
                    st.session_state.followup_answers[q_id] = answer
                else:
                    all_answered = False
            
            st.divider()
        
        # Generate report button
        if len(st.session_state.followup_answers) >= len(followup_questions) - 1:
            if st.button("📊 Generate Detailed Report", use_container_width=True, type="primary"):
                st.session_state.report_generated = True
                st.rerun()
        else:
            st.info(f"Please answer at least {len(followup_questions) - 1} of {len(followup_questions)} questions")
    
    # Step 4: Display final report
    if st.session_state.report_generated:
        st.markdown("## Step 4️⃣ Detailed Analysis Report")
        
        with st.spinner("📊 Generating comprehensive report..."):
            try:
                classifier = IssueClassifier(api_key)
                report = classifier.generate_report({
                    "user_issue": st.session_state.user_issue,
                    "classification": st.session_state.issue_classification,
                    "followup_answers": st.session_state.followup_answers
                })
                st.session_state.final_report = report
                
            except Exception as e:
                st.error(f"Error generating report: {e}")
                return
        
        report = st.session_state.final_report
        
        # Analysis section
        st.markdown("### 📋 Detailed Analysis")
        st.write(report.get("analysis", "Analysis in progress..."))
        
        # Root causes
        if report.get("root_causes"):
            st.markdown("### 🔍 Root Causes")
            for i, cause in enumerate(report.get("root_causes", []), 1):
                st.write(f"{i}. {cause}")
        
        # Immediate actions
        if report.get("immediate_actions"):
            st.markdown("### 🚨 Immediate Actions (High Priority)")
            for action in report.get("immediate_actions", []):
                with st.container(border=True):
                    st.markdown(f"**🔴 {action.get('action', 'Action')}**")
                    st.caption(f"Why: {action.get('why', '')}")
        
        # Medium term steps
        if report.get("medium_term_steps"):
            st.markdown("### ⏱️ Medium-Term Steps")
            for step in report.get("medium_term_steps", []):
                with st.container(border=True):
                    priority_icon = {"high": "🟠", "medium": "🟡", "low": "🟢"}
                    icon = priority_icon.get(step.get("priority", "medium"), "🔵")
                    st.markdown(f"**{icon} {step.get('action', 'Step')}**")
                    st.caption(f"Why: {step.get('why', '')}")
        
        # Recommended tools
        if report.get("tools_recommended"):
            st.markdown("### 🛠️ Recommended Tools & Services")
            cols = st.columns(2)
            for i, tool in enumerate(report.get("tools_recommended", [])):
                with cols[i % 2]:
                    st.write(f"• {tool}")
        
        # Timeline
        if report.get("timeline"):
            st.markdown("### ⏳ Implementation Timeline")
            st.info(report.get("timeline", ""))
        
        # FAQ
        if report.get("faq"):
            st.markdown("### ❓ Frequently Asked Questions")
            for faq in report.get("faq", []):
                with st.expander(faq.get("question", "Question")):
                    st.write(faq.get("answer", ""))
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Analyze Another Issue", use_container_width=True):
                st.session_state.user_issue = None
                st.session_state.issue_classified = False
                st.session_state.issue_classification = None
                st.session_state.followup_questions = []
                st.session_state.followup_answers = {}
                st.session_state.report_generated = False
                st.session_state.final_report = None
                st.rerun()
        
        with col2:
            if st.button("📖 View Assessment Path", use_container_width=True):
                with st.expander("Assessment Journey"):
                    st.write("**Your Issue:**")
                    st.write(st.session_state.user_issue)
                    st.divider()
                    st.write("**Follow-up Answers:**")
                    for q_id, answer in st.session_state.followup_answers.items():
                        st.write(f"- {q_id}: {answer}")




if __name__ == "__main__":
    main()

