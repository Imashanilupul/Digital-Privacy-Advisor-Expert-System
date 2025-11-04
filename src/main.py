"""
Main entry point for Digital Privacy Advisor expert system.
Provides a chat-like conversational interface for privacy assessment.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference_engine import InferenceEngine
from src.chat_interface import ChatInterface


def main():
    """Run the privacy advisor as an interactive chat."""
    engine = InferenceEngine()
    chat = ChatInterface(engine)
    success = chat.run()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())