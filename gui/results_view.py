"""
Results view for displaying recommendations
"""

import tkinter as tk
from tkinter import ttk, filedialog
from src.utils import get_risk_color, format_report

class ResultsView(tk.Frame):
    """Results display view"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.results = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create results widgets"""
        # Create scrollable canvas
        self.canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def display_results(self, results):
        """Display analysis results"""
        self.results = results
        
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.scrollable_frame, bg='#1e40af', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = tk.Label(
            header_frame,
            text="Privacy Assessment Results",
            font=('Helvetica', 20, 'bold'),
            bg='#1e40af',
            fg='white'
        )
        title.pack(pady=15)
        
        # Risk Level Banner
        risk_color = get_risk_color(results['risk_level'])
        risk_frame = tk.Frame(self.scrollable_frame, bg=risk_color, relief='raised', bd=2)
        risk_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        risk_title = tk.Label(
            risk_frame,
            text=f"⚠ Risk Level: {results['risk_level']}",
            font=('Helvetica', 18, 'bold'),
            bg=risk_color,
            fg='white'
        )
        risk_title.pack(pady=10)
        
        risk_desc = self._get_risk_description(results['risk_level'])
        risk_label = tk.Label(
            risk_frame,
            text=risk_desc,
            font=('Helvetica', 11),
            bg=risk_color,
            fg='white',
            wraplength=600
        )
        risk_label.pack(pady=(0, 10), padx=20)
        
        # Statistics
        stats_frame = tk.Frame(self.scrollable_frame, bg='#f3f4f6', relief='solid', bd=1)
        stats_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        stats = results['stats']
        stats_text = f"""
        Total Recommendations: {stats['total']}  |  High Priority: {stats['high_priority']}  |  Medium: {stats['medium_priority']}  |  Low: {stats['low_priority']}
        """
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text.strip(),
            font=('Helvetica', 10, 'bold'),
            bg='#f3f4f6',
            fg='#374151'
        )
        stats_label.pack(pady=10)
        
        # Recommendations Section
        rec_title = tk.Label(
            self.scrollable_frame,
            text="📋 Personalized Recommendations",
            font=('Helvetica', 16, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        rec_title.pack(anchor='w', padx=20, pady=(10, 20))
        
        # Display each recommendation
        for idx, rec in enumerate(results['recommendations'], 1):
            self._create_recommendation_card(idx, rec)
        
        # Next Steps Section
        self._create_next_steps_section()
    
    def _create_recommendation_card(self, index, rec):
        """Create a card for a single recommendation"""
        # Main card frame
        card = tk.Frame(
            self.scrollable_frame,
            bg='white',
            relief='solid',
            bd=1,
            highlightbackground='#e5e7eb',
            highlightthickness=2
        )
        card.pack(fill='x', padx=20, pady=10)
        
        # Header with priority badge
        header = tk.Frame(card, bg='white')
        header.pack(fill='x', padx=15, pady=(15, 10))
        
        # Index number
        index_label = tk.Label(
            header,
            text=f"#{index}",
            font=('Helvetica', 16, 'bold'),
            bg='white',
            fg='#9ca3af'
        )
        index_label.pack(side='left', padx=(0, 10))
        
        # Priority badge
        priority_colors = {
            'high': ('#fecaca', '#991b1b'),
            'medium': ('#fef3c7', '#92400e'),
            'low': ('#bfdbfe', '#1e3a8a')
        }
        bg_color, fg_color = priority_colors.get(rec['priority'], ('#e5e7eb', '#374151'))
        
        priority_badge = tk.Label(
            header,
            text=f"{rec['priority'].upper()} PRIORITY",
            font=('Helvetica', 9, 'bold'),
            bg=bg_color,
            fg=fg_color,
            padx=8,
            pady=3,
            relief='solid',
            bd=1
        )
        priority_badge.pack(side='left')
        
        # Category
        category_label = tk.Label(
            header,
            text=rec['category'],
            font=('Helvetica', 9),
            bg='white',
            fg='#6b7280'
        )
        category_label.pack(side='left', padx=(10, 0))
        
        # Message
        message_label = tk.Label(
            card,
            text=rec['message'],
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#1f2937',
            wraplength=700,
            justify='left'
        )
        message_label.pack(anchor='w', padx=15, pady=(5, 10))
        
        # Details box
        details_frame = tk.Frame(card, bg='#dbeafe', relief='solid', bd=1)
        details_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        details_icon = tk.Label(
            details_frame,
            text="ℹ️",
            font=('Helvetica', 12),
            bg='#dbeafe'
        )
        details_icon.pack(side='left', padx=(10, 5), pady=10)
        
        details_label = tk.Label(
            details_frame,
            text=rec['details'],
            font=('Helvetica', 10),
            bg='#dbeafe',
            fg='#1e3a8a',
            wraplength=650,
            justify='left'
        )
        details_label.pack(side='left', padx=(5, 10), pady=10, fill='x', expand=True)
        
        # Action box
        action_frame = tk.Frame(card, bg='#d1fae5', relief='solid', bd=1)
        action_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        action_icon = tk.Label(
            action_frame,
            text="✓",
            font=('Helvetica', 12, 'bold'),
            bg='#d1fae5',
            fg='#065f46'
        )
        action_icon.pack(side='left', padx=(10, 5), pady=10)
        
        action_title = tk.Label(
            action_frame,
            text="Action Step:",
            font=('Helvetica', 10, 'bold'),
            bg='#d1fae5',
            fg='#065f46'
        )
        action_title.pack(anchor='w', padx=(5, 10), pady=(10, 2))
        
        action_label = tk.Label(
            action_frame,
            text=rec['action'],
            font=('Helvetica', 10),
            bg='#d1fae5',
            fg='#065f46',
            wraplength=650,
            justify='left'
        )
        action_label.pack(anchor='w', padx=(5, 10), pady=(0, 10), fill='x')
    
    def _create_next_steps_section(self):
        """Create next steps section"""
        # Section frame
        section_frame = tk.Frame(
            self.scrollable_frame,
            bg='#ede9fe',
            relief='solid',
            bd=2
        )
        section_frame.pack(fill='x', padx=20, pady=20)
        
        title = tk.Label(
            section_frame,
            text="📌 Next Steps",
            font=('Helvetica', 14, 'bold'),
            bg='#ede9fe',
            fg='#5b21b6'
        )
        title.pack(anchor='w', padx=15, pady=(15, 10))
        
        steps = [
            "Start with high-priority recommendations first",
            "Implement changes gradually over the next 30 days",
            "Re-assess your security practices quarterly",
            "Stay informed about emerging privacy and security threats",
            "Share this tool with family and friends to help them stay secure"
        ]
        
        for step in steps:
            step_label = tk.Label(
                section_frame,
                text=f"• {step}",
                font=('Helvetica', 10),
                bg='#ede9fe',
                fg='#5b21b6',
                wraplength=700,
                justify='left'
            )
            step_label.pack(anchor='w', padx=30, pady=3)
        
        # Add spacing
        tk.Label(section_frame, text="", bg='#ede9fe').pack(pady=5)
    
    def _get_risk_description(self, risk_level):
        """Get description for risk level"""
        descriptions = {
            'Critical': 'Your digital security needs immediate attention. Follow all high-priority recommendations as soon as possible.',
            'High': 'Your security has significant vulnerabilities. Address high-priority items first to protect yourself.',
            'Medium': 'Your security is adequate but has room for improvement. Follow the recommendations to strengthen your privacy.',
            'Low': 'Your digital security practices are good. Keep following best practices and stay vigilant!'
        }
        return descriptions.get(risk_level, 'Assessment complete.')
    
    def export_report(self):
        """Export results to a text file"""
        if not self.results:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Privacy Assessment Report"
        )
        
        if filename:
            report = format_report(
                self.results['user_data'],
                self.results['recommendations'],
                self.results['risk_level'],
                self.results['risk_score']
            )
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            return True
        return False