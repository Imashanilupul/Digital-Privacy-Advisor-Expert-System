"""
Chat-like interface for the expert system.
Provides an interactive, conversational Q&A flow for privacy assessment.
"""

from typing import Dict, List, Any


class ChatInterface:
    """Interactive chat-based interface for the privacy expert system."""

    def __init__(self, inference_engine):
        """
        Initialize the chat interface.
        
        Args:
            inference_engine: The inference engine (e.g., InferenceEngine from src/inference_engine.py)
        """
        self.inference_engine = inference_engine
        self.user_data = {}
        self.questions = [
            {
                "key": "password_reuse",
                "question": "Do you reuse passwords across different accounts?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "password_manager",
                "question": "Do you use a password manager to store your passwords?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "two_factor",
                "question": "Do you have two-factor authentication (2FA) enabled on important accounts?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "public_wifi",
                "question": "Do you connect to public Wi-Fi networks (cafes, airports, etc.)?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "vpn",
                "question": "Do you use a VPN when accessing the internet?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "os_update",
                "question": "Do you keep your operating system and apps up to date?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "backup_data",
                "question": "Do you regularly back up your important data?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "email_encryption",
                "question": "Do you use email encryption for sensitive communications?",
                "help": "(yes/no)",
                "type": "yes_no"
            },
            {
                "key": "app_permissions",
                "question": "List app permissions you grant (e.g., Location Contacts Camera Microphone) or type 'None':",
                "help": "Enter space-separated permissions or 'None'",
                "type": "multislot"
            },
            {
                "key": "social_media",
                "question": "List social media platforms you use (e.g., Facebook Instagram Twitter) or type 'None':",
                "help": "Enter space-separated platform names or 'None'",
                "type": "multislot"
            }
        ]

    def _parse_yes_no(self, response: str) -> str:
        """Parse yes/no response to lowercase."""
        r = response.strip().lower()
        if r in ("yes", "y"):
            return "yes"
        elif r in ("no", "n"):
            return "no"
        else:
            return None

    def _parse_multislot(self, response: str) -> List[str]:
        """Parse multislot response (space-separated values)."""
        r = response.strip()
        if r.lower() == "none":
            return []
        return r.split()

    def run(self):
        """Run the interactive chat interview."""
        print("\n" + "=" * 70)
        print("  Digital Privacy Advisor - Privacy Assessment Chat")
        print("=" * 70)
        print("\nWelcome! I'm here to assess your digital privacy and security.")
        print("Please answer the following questions honestly.\n")
        print("(You can type 'quit' or 'exit' at any time to cancel.)\n")

        for q_obj in self.questions:
            key = q_obj["key"]
            question = q_obj["question"]
            q_type = q_obj["type"]
            help_text = q_obj["help"]

            while True:
                print(f"\n[Q{self.questions.index(q_obj) + 1}/{len(self.questions)}] {question}")
                print(f"  {help_text}")
                response = input("You: ").strip()

                # Allow early exit
                if response.lower() in ("quit", "exit"):
                    print("\nInterview cancelled. Goodbye!")
                    return False

                # Parse and validate
                if q_type == "yes_no":
                    parsed = self._parse_yes_no(response)
                    if parsed is None:
                        print("  ❌ Please enter 'yes' or 'no'.")
                        continue
                    self.user_data[key] = parsed
                    print(f"  ✓ Got it: {parsed}")
                    break
                elif q_type == "multislot":
                    parsed = self._parse_multislot(response)
                    self.user_data[key] = parsed
                    if parsed:
                        print(f"  ✓ Got it: {', '.join(parsed)}")
                    else:
                        print(f"  ✓ Got it: (no items)")
                    break

        # Run inference
        print("\n" + "=" * 70)
        print("Analyzing your responses...")
        print("=" * 70 + "\n")

        recommendations, risk_score = self.inference_engine.process(self.user_data)

        # Display results
        self._display_results(recommendations, risk_score)
        return True

    def _display_results(self, recommendations: List[Dict[str, Any]], risk_score: int):
        """Display recommendations in a friendly chat format."""
        if not recommendations:
            print("Great! Based on your answers, you don't have any immediate recommendations.\n")
            print(f"Overall Risk Score: {risk_score}/100\n")
            return

        # Sort by priority and risk score
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_recs = sorted(
            recommendations,
            key=lambda r: (priority_order.get(r["priority"], 3), -r["risk_score"])
        )

        # Categorize by priority
        high_priority = [r for r in sorted_recs if r["priority"] == "high"]
        medium_priority = [r for r in sorted_recs if r["priority"] == "medium"]
        low_priority = [r for r in sorted_recs if r["priority"] == "low"]

        print(f"Overall Risk Score: {risk_score}/100\n")

        if high_priority:
            print("🔴 HIGH PRIORITY - Address these immediately:\n")
            for i, rec in enumerate(high_priority, 1):
                self._print_recommendation(rec, i)

        if medium_priority:
            print("\n🟡 MEDIUM PRIORITY - Consider these improvements:\n")
            for i, rec in enumerate(medium_priority, 1):
                self._print_recommendation(rec, i)

        if low_priority:
            print("\n🟢 LOW PRIORITY - Nice to have:\n")
            for i, rec in enumerate(low_priority, 1):
                self._print_recommendation(rec, i)

        print("\n" + "=" * 70)
        print("Thank you for using the Digital Privacy Advisor!")
        print("=" * 70 + "\n")

    def _print_recommendation(self, rec: Dict[str, Any], index: int):
        """Print a single recommendation in a friendly format."""
        print(f"{index}. {rec['message']}")
        print(f"   Category: {rec['category']}")
        print(f"   Details: {rec['details']}")
        print(f"   Action: {rec['action']}")
        print(f"   Risk Score: +{rec['risk_score']}\n")
