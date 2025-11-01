"""
Dialog windows for the application
"""

import tkinter as tk
from tkinter import messagebox

class AboutDialog:
    """About dialog"""
    
    @staticmethod
    def show(parent):
        """Show about dialog"""
        messagebox.showinfo(
            "About Digital Privacy Advisor",
            "Digital Privacy Advisor v1.0.0\n\n"
            "An expert system for assessing and improving\n"
            "your digital privacy and security.\n\n"
            "© 2024 Digital Privacy Advisor Team"
        )

class ErrorDialog:
    """Error dialog"""
    
    @staticmethod
    def show(parent, message):
        """Show error dialog"""
        messagebox.showerror("Error", message)

class ConfirmDialog:
    """Confirmation dialog"""
    
    @staticmethod
    def show(parent, message):
        """Show confirmation dialog"""
        return messagebox.askyesno("Confirm", message)

class InfoDialog:
    """Information dialog"""
    
    @staticmethod
    def show(parent, message):
        """Show info dialog"""
        messagebox.showinfo("Information", message)
