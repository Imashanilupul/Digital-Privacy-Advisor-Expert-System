"""
Output handler for processing and formatting recommendations
"""

from src.utils import sort_recommendations, calculate_risk_level

class OutputHandler:
    """Handles output processing and formatting"""
    
    def __init__(self):
        self.recommendations = []
        self.risk_score = 0
        self.risk_level = "Low"
    
    def process_results(self, recommendations, risk_score):
        """
        Process inference engine results
        
        Args:
            recommendations (list): Raw recommendations
            risk_score (int): Total risk score
            
        Returns:
            tuple: (sorted_recommendations, risk_level)
        """
        self.recommendations = sort_recommendations(recommendations)
        self.risk_score = risk_score
        self.risk_level = calculate_risk_level(risk_score)
        
        return self.recommendations, self.risk_level
    
    def get_summary_stats(self):
        """
        Get summary statistics
        
        Returns:
            dict: Summary stats
        """
        priority_counts = {'high': 0, 'medium': 0, 'low': 0}
        for rec in self.recommendations:
            priority = rec.get('priority', 'low')
            priority_counts[priority] += 1
        
        return {
            'total': len(self.recommendations),
            'high_priority': priority_counts['high'],
            'medium_priority': priority_counts['medium'],
            'low_priority': priority_counts['low'],
            'risk_score': self.risk_score,
            'risk_level': self.risk_level
        }
