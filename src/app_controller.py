"""
Application controller - coordinates GUI and inference engine
"""

from src.input_handler import InputHandler
from src.inference_engine import InferenceEngine
from src.output_handler import OutputHandler

class AppController:
    """Main application controller"""
    
    def __init__(self):
        self.input_handler = InputHandler()
        self.inference_engine = InferenceEngine()
        self.output_handler = OutputHandler()
    
    def update_input(self, field, value):
        """Update a single input field"""
        self.input_handler.update_field(field, value)
    
    def toggle_multi_input(self, field, value):
        """Toggle a multi-select input"""
        self.input_handler.toggle_multi_select(field, value)
    
    def validate_inputs(self):
        """Validate all inputs"""
        return self.input_handler.validate_data()
    
    def run_analysis(self):
        """
        Run the security analysis
        
        Returns:
            dict: Analysis results
        """
        user_data = self.input_handler.get_data()
        recommendations, risk_score = self.inference_engine.process(user_data)
        sorted_recs, risk_level = self.output_handler.process_results(recommendations, risk_score)
        
        return {
            'recommendations': sorted_recs,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'stats': self.output_handler.get_summary_stats(),
            'user_data': user_data
        }
    
    def reset(self):
        """Reset the controller"""
        self.input_handler.reset()
