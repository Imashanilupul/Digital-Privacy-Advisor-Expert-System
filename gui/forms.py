"""
Input forms for user data collection
"""

import tkinter as tk
from tkinter import ttk

class InputForm(tk.Frame):
    """Main input form for collecting user data"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        """Create form widgets"""
        # Create scrollable canvas
        canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title = tk.Label(
            scrollable_frame,
            text="Digital Privacy Assessment",
            font=('Helvetica', 20, 'bold'),
            bg='white',
            fg='#1e40af'
        )
        title.pack(pady=20, padx=20)
        
        subtitle = tk.Label(
            scrollable_frame,
            text="Answer these questions honestly to receive personalized security recommendations",
            font=('Helvetica', 10),
            bg='white',
            fg='#6b7280'
        )
        subtitle.pack(pady=(0, 30), padx=20)
        
        # Social Media
        self._create_multi_select_section(
            scrollable_frame,
            "Which social media platforms do you use regularly?",
            'social_media',
            ['Facebook', 'Instagram', 'Twitter/X', 'TikTok', 'LinkedIn', 'Snapchat']
        )
        
        # Devices
        self._create_multi_select_section(
            scrollable_frame,
            "Which devices do you use?",
            'devices',
            ['Smartphone', 'Laptop', 'Tablet', 'Desktop', 'Smart TV', 'IoT Devices']
        )
        
        # Password Questions
        self._create_yes_no_section(
            scrollable_frame,
            "Do you reuse passwords across multiple accounts?",
            'password_reuse'
        )
        
        self._create_yes_no_section(
            scrollable_frame,
            "Do you use a password manager?",
            'password_manager'
        )
        
        # 2FA
        self._create_yes_no_section(
            scrollable_frame,
            "Do you use Two-Factor Authentication (2FA) on important accounts?",
            'two_factor'
        )
        
        # Network
        self._create_yes_no_section(
            scrollable_frame,
            "Do you regularly use public Wi-Fi?",
            'public_wifi'
        )
        
        self._create_yes_no_section(
            scrollable_frame,
            "Do you use a VPN?",
            'vpn'
        )
        
        # Updates
        self._create_yes_no_section(
            scrollable_frame,
            "Do you regularly update your operating system and apps?",
            'os_update'
        )
        
        # Permissions
        self._create_multi_select_section(
            scrollable_frame,
            "Which app permissions have you granted on your devices?",
            'app_permissions',
            ['Location', 'Contacts', 'Camera', 'Microphone', 'Storage', 'None']
        )
        
        # Backup
        self._create_yes_no_section(
            scrollable_frame,
            "Do you regularly backup your important data?",
            'backup_data'
        )
        
        # Email Encryption
        self._create_yes_no_section(
            scrollable_frame,
            "Do you use email encryption for sensitive communications?",
            'email_encryption'
        )
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def _create_multi_select_section(self, parent, question, field, options):
        """Create a multi-select question section"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', padx=20, pady=15)
        
        # Question
        label = tk.Label(
            frame,
            text=question,
            font=('Helvetica', 11, 'bold'),
            bg='white',
            fg='#1f2937',
            wraplength=600,
            justify='left'
        )
        label.pack(anchor='w', pady=(0, 10))
        
        # Options frame
        options_frame = tk.Frame(frame, bg='white')
        options_frame.pack(fill='x')
        
        # Create checkbuttons
        for i, option in enumerate(options):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                options_frame,
                text=option,
                variable=var,
                font=('Helvetica', 10),
                bg='white',
                activebackground='white',
                command=lambda opt=option: self.controller.toggle_multi_input(field, opt)
            )
            cb.grid(row=i//2, column=i%2, sticky='w', padx=5, pady=5)
        
        # Separator
        sep = ttk.Separator(frame, orient='horizontal')
        sep.pack(fill='x', pady=(15, 0))
    
    def _create_yes_no_section(self, parent, question, field):
        """Create a yes/no question section"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', padx=20, pady=15)
        
        # Question
        label = tk.Label(
            frame,
            text=question,
            font=('Helvetica', 11, 'bold'),
            bg='white',
            fg='#1f2937',
            wraplength=600,
            justify='left'
        )
        label.pack(anchor='w', pady=(0, 10))
        
        # Options frame
        options_frame = tk.Frame(frame, bg='white')
        options_frame.pack(anchor='w')
        
        # Radio buttons
        var = tk.StringVar(value="")
        for option in ['yes', 'no']:
            rb = tk.Radiobutton(
                options_frame,
                text=option.capitalize(),
                variable=var,
                value=option,
                font=('Helvetica', 10),
                bg='white',
                activebackground='white',
                command=lambda f=field, v=var: self.controller.update_input(f, v.get())
            )
            rb.pack(side='left', padx=10)
        
        # Separator
        sep = ttk.Separator(frame, orient='horizontal')
        sep.pack(fill='x', pady=(15, 0))
