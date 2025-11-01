"""
Input handler for collecting and validating user data
"""

class InputHandler:
    """Handles user input collection and validation"""
    
    def __init__(self):
        self.user_data = {
            'social_media': [],
            'devices': [],
            'password_reuse': None,
            'password_manager': None,
            'two_factor': None,
            'public_wifi': None,
            'vpn': None,
            'os_update': None,
            'app_permissions': [],
            'backup_data': None,
            'email_encryption': None
        }
    
    def update_field(self, field, value):
        """Update a single field in user data"""
        self.user_data[field] = value
    
    def toggle_multi_select(self, field, value):
        """Toggle a value in a multi-select field"""
        if value in self.user_data[field]:
            self.user_data[field].remove(value)
        else:
            self.user_data[field].append(value)
    
    def validate_data(self):
        """
        Validate that all required fields are filled
        
        Returns:
            tuple: (is_valid, error_message)
        """
        required_single = [
            'password_reuse', 'password_manager', 'two_factor',
            'public_wifi', 'vpn', 'os_update', 'backup_data', 'email_encryption'
        ]
        
        for field in required_single:
            if self.user_data[field] is None:
                return False, f"Please answer the question about {field.replace('_', ' ')}"
        
        return True, ""
    
    def get_data(self):
        """Get the current user data"""
        return self.user_data.copy()
    
    def reset(self):
        """Reset all user data to initial state"""
        self.__init__()