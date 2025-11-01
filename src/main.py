"""
Main entry point for Digital Privacy Advisor application
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.main_window import MainWindow

def main():
    """Main function"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()