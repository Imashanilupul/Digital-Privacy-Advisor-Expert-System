"""
Streamlit GUI for Digital Privacy Advisor Expert System.
Provides an interactive, conversational chat-based privacy assessment interface.
"""

import streamlit as st
from typing import Dict, List, Any
from src.inference_engine import InferenceEngine


# Configure page
st.set_page_config(
    page_title="Digital Privacy Advisor",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    # Header
    st.markdown("# 🔒 Digital Privacy Advisor")
    st.markdown("*Assess your digital privacy and security posture with personalized recommendations*")
    
    # Assessment flow
    if not st.session_state.assessment_complete:
        questions = get_questions()
        total_questions = len(questions)
        
        # Progress bar
        progress = st.session_state.current_question / total_questions
        st.progress(progress)
        
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
