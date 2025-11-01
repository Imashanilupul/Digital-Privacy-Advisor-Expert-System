"""
Main application window
"""

import tkinter as tk
from tkinter import ttk
from gui.forms import InputForm
from gui.results_view import ResultsView
from gui.dialogs import AboutDialog, ErrorDialog, InfoDialog, ConfirmDialog
from src.app_controller import AppController

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital Privacy Advisor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("resources/icons/logo.ico")
        except:
            pass
        
        # Initialize controller
        self.controller = AppController()
        
        # Current view
        self.current_view = 'input'
        
        # Create UI
        self.create_menu()
        self.create_toolbar()
        self.create_main_area()
        self.create_statusbar()
        
        # Show input form initially
        self.show_input_form()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Assessment", command=self.new_assessment)
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: AboutDialog.show(self.root))
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = tk.Frame(self.root, bg='#1e40af', relief='raised', bd=2)
        toolbar.pack(side='top', fill='x')
        
        # Title
        title = tk.Label(
            toolbar,
            text="🛡️ Digital Privacy Advisor",
            font=('Helvetica', 16, 'bold'),
            bg='#1e40af',
            fg='white'
        )
        title.pack(side='left', padx=20, pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(toolbar, bg='#1e40af')
        btn_frame.pack(side='right', padx=10)
        
        # Analyze button (initially hidden, shown in input view)
        self.analyze_btn = tk.Button(
            btn_frame,
            text="🔍 Analyze Security",
            font=('Helvetica', 11, 'bold'),
            bg='#10b981',
            fg='white',
            activebackground='#059669',
            activeforeground='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.analyze_security
        )
        
        # Export button (initially hidden, shown in results view)
        self.export_btn = tk.Button(
            btn_frame,
            text="💾 Export Report",
            font=('Helvetica', 11, 'bold'),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            activeforeground='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.export_report
        )
        
        # New Assessment button (initially hidden, shown in results view)
        self.new_btn = tk.Button(
            btn_frame,
            text="🔄 New Assessment",
            font=('Helvetica', 11, 'bold'),
            bg='#6b7280',
            fg='white',
            activebackground='#4b5563',
            activeforeground='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.new_assessment
        )
    
    def create_main_area(self):
        """Create main content area"""
        self.main_frame = tk.Frame(self.root, bg='#f3f4f6')
        self.main_frame.pack(side='top', fill='both', expand=True)
    
    def create_statusbar(self):
        """Create status bar"""
        self.statusbar = tk.Label(
            self.root,
            text="Ready",
            font=('Helvetica', 9),
            bg='#e5e7eb',
            fg='#374151',
            anchor='w',
            relief='sunken',
            bd=1
        )
        self.statusbar.pack(side='bottom', fill='x')
    
    def show_input_form(self):
        """Show input form"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create input form
        self.input_form = InputForm(self.main_frame, self.controller)
        self.input_form.pack(fill='both', expand=True)
        
        # Update toolbar buttons
        self.analyze_btn.pack(side='right', padx=5)
        self.export_btn.pack_forget()
        self.new_btn.pack_forget()
        
        self.current_view = 'input'
        self.update_status("Fill out the assessment form")
    
    def show_results(self, results):
        """Show results view"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create results view
        self.results_view = ResultsView(self.main_frame, self.controller)
        self.results_view.pack(fill='both', expand=True)
        self.results_view.display_results(results)
        
        # Update toolbar buttons
        self.analyze_btn.pack_forget()
        self.export_btn.pack(side='right', padx=5)
        self.new_btn.pack(side='right', padx=5)
        
        self.current_view = 'results'
        self.update_status(f"Analysis complete - Risk Level: {results['risk_level']}")
    
    def analyze_security(self):
        """Run security analysis"""
        # Validate inputs
        is_valid, error_msg = self.controller.validate_inputs()
        
        if not is_valid:
            ErrorDialog.show(self.root, f"Please complete all questions.\n\n{error_msg}")
            return
        
        # Update status
        self.update_status("Analyzing your security...")
        self.root.update()
        
        # Run analysis
        try:
            results = self.controller.run_analysis()
            self.show_results(results)
        except Exception as e:
            ErrorDialog.show(self.root, f"An error occurred during analysis:\n{str(e)}")
            self.update_status("Analysis failed")
    
    def export_report(self):
        """Export assessment report"""
        if self.current_view == 'results' and hasattr(self, 'results_view'):
            success = self.results_view.export_report()
            if success:
                InfoDialog.show(self.root, "Report exported successfully!")
                self.update_status("Report exported")
        else:
            ErrorDialog.show(self.root, "No results to export. Please run an analysis first.")
    
    def new_assessment(self):
        """Start a new assessment"""
        if self.current_view == 'results':
            confirm = ConfirmDialog.show(
                self.root,
                "Are you sure you want to start a new assessment?\nCurrent results will be cleared."
            )
            if not confirm:
                return
        
        self.controller.reset()
        self.show_input_form()
        self.update_status("New assessment started")
    
    def update_status(self, message):
        """Update status bar message"""
        self.statusbar.config(text=message)
    
    def quit_app(self):
        """Quit the application"""
        if ConfirmDialog.show(self.root, "Are you sure you want to exit?"):
            self.root.quit()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()