"""
AI-Powered Issue Classification and Analysis System
Uses Gemini API to classify privacy issues and generate targeted follow-up questions
"""

import google.generativeai as genai
from typing import Dict, List, Any
import json
import re


class IssueClassifier:
    """Classifies privacy issues using Gemini AI and generates follow-up questions"""
    
    CATEGORIES = {
        "password_security": "🔐 Password Security",
        "account_security": "👤 Account Security",
        "network_security": "🌐 Network Security",
        "device_security": "💻 Device Security",
        "data_protection": "📁 Data Protection",
        "communication_security": "📧 Communication Security",
        "privacy_settings": "⚙️ Privacy Settings",
        "social_media": "📱 Social Media",
        "general": "❓ General Privacy"
    }
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def classify_issue(self, user_issue: str) -> Dict[str, Any]:
        """
        Classify a user's privacy issue into categories
        
        Returns:
            Dict with classification, severity, key concerns, and risk level
        """
        categories_str = "\n".join([f"- {key}: {value}" for key, value in self.CATEGORIES.items()])
        
        prompt = f"""You are a privacy and security expert. Analyze this user's privacy concern:

"{user_issue}"

Provide a structured JSON response with:
{{
    "primary_category": "one of: password_security, account_security, network_security, device_security, data_protection, communication_security, privacy_settings, social_media, general",
    "secondary_categories": ["list of other relevant categories"],
    "severity": "low, medium, high, or critical",
    "risk_level": 0-100 (numerical risk score),
    "summary": "2-3 sentence summary of the issue",
    "key_concerns": ["concern1", "concern2", "concern3"],
    "affected_areas": ["area1", "area2"]
}}

Return ONLY the JSON, no other text."""
        
        try:
            response = self.model.generate_content(prompt)
            # Clean markdown formatting
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            
            classification = json.loads(text)
            return classification
        except Exception as e:
            return {
                "primary_category": "general",
                "secondary_categories": [],
                "severity": "medium",
                "risk_level": 50,
                "summary": "Issue identified. Please provide more details.",
                "key_concerns": ["Unable to fully analyze issue"],
                "affected_areas": [],
                "error": str(e)
            }
    
    def generate_followup_questions(self, classification: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate targeted follow-up questions based on issue classification
        
        Returns:
            List of follow-up question dicts with id, question, type, options, context
        """
        concerns = "\n".join(classification.get("key_concerns", []))
        category = classification.get("primary_category", "general")
        summary = classification.get("summary", "")
        
        prompt = f"""Based on this privacy issue classification, generate 4-5 focused follow-up questions to clarify the user's situation:

Category: {category}
Summary: {summary}
Key Concerns: {concerns}

For EACH question, provide a JSON object with:
{{
    "id": "q1", "q2", etc,
    "question": "specific, clear question",
    "type": "yes_no", "choice", or "text",
    "options": ["only if type is choice"],
    "context": "brief explanation why we're asking"
}}

Return a JSON array of questions. ONLY return the JSON array, no other text.

Example format:
[
  {{"id": "q1", "question": "...", "type": "yes_no", "context": "..."}},
  {{"id": "q2", "question": "...", "type": "choice", "options": ["opt1", "opt2"], "context": "..."}}
]"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean markdown
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            
            questions = json.loads(text)
            return questions
        except Exception as e:
            return [
                {
                    "id": "q1",
                    "question": "Can you provide more details about when you first noticed this issue?",
                    "type": "text",
                    "context": "Understanding timeline helps us assess urgency"
                },
                {
                    "id": "q2",
                    "question": "What devices are affected by this concern?",
                    "type": "choice",
                    "options": ["Computer", "Mobile", "All devices", "Not sure"],
                    "context": "Device type affects security recommendations"
                }
            ]
    
    def generate_report(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate detailed report with analysis and recommendations
        
        Args:
            issue_data: Dict with user_issue, classification, followup_answers
        
        Returns:
            Dict with detailed analysis and recommendations
        """
        user_issue = issue_data.get("user_issue", "")
        classification = issue_data.get("classification", {})
        followup_answers = issue_data.get("followup_answers", {})
        
        # Compile all information
        answers_str = "\n".join([f"Q: {k}\nA: {v}" for k, v in followup_answers.items()])
        
        prompt = f"""You are a privacy and security expert. Provide a detailed analysis report for this privacy concern:

USER'S ISSUE: {user_issue}

CLASSIFICATION:
- Category: {classification.get('primary_category', 'general')}
- Severity: {classification.get('severity', 'medium')}
- Risk Level: {classification.get('risk_level', 50)}/100

FOLLOW-UP ANSWERS:
{answers_str}

Generate a comprehensive JSON report with:
{{
    "analysis": "Detailed 2-3 paragraph analysis of the issue and risks",
    "root_causes": ["root cause 1", "root cause 2"],
    "immediate_actions": [
        {{"priority": "high", "action": "...", "why": "..."}}
    ],
    "medium_term_steps": [
        {{"priority": "medium", "action": "...", "why": "..."}}
    ],
    "tools_recommended": ["tool1", "tool2"],
    "timeline": "Suggested timeline for implementing changes",
    "faq": [
        {{"question": "...", "answer": "..."}}
    ]
}}

Return ONLY valid JSON, no other text."""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean markdown
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            
            report = json.loads(text)
            return report
        except Exception as e:
            return {
                "analysis": "Analysis in progress. Please try again.",
                "root_causes": [],
                "immediate_actions": [],
                "medium_term_steps": [],
                "tools_recommended": [],
                "timeline": "Contact support",
                "faq": [],
                "error": str(e)
            }
    
    def get_category_icon(self, category: str) -> str:
        """Get emoji icon for a category"""
        icon_map = {
            "password_security": "🔐",
            "account_security": "👤",
            "network_security": "🌐",
            "device_security": "💻",
            "data_protection": "📁",
            "communication_security": "📧",
            "privacy_settings": "⚙️",
            "social_media": "📱",
            "general": "❓"
        }
        return icon_map.get(category, "🔒")
