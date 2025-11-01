"""
Inference engine - processes user data and generates recommendations
"""

class InferenceEngine:
    """
    Expert system inference engine
    Note: This is a pure Python implementation.
    For CLIPS integration, you would use clipspy library.
    """
    
    def __init__(self):
        self.recommendations = []
        self.risk_score = 0
    
    def process(self, user_data):
        """
        Process user data through rule-based system
        
        Args:
            user_data (dict): User input data
            
        Returns:
            tuple: (recommendations, risk_score)
        """
        self.recommendations = []
        self.risk_score = 0
        
        # Apply rules
        self._check_password_rules(user_data)
        self._check_2fa_rules(user_data)
        self._check_network_rules(user_data)
        self._check_device_rules(user_data)
        self._check_privacy_rules(user_data)
        self._check_social_media_rules(user_data)
        self._check_backup_rules(user_data)
        self._check_encryption_rules(user_data)
        
        return self.recommendations, self.risk_score
    
    def _add_recommendation(self, priority, category, message, details, action, risk_score):
        """Add a recommendation and update risk score"""
        self.recommendations.append({
            'priority': priority,
            'category': category,
            'message': message,
            'details': details,
            'action': action,
            'risk_score': risk_score
        })
        self.risk_score += risk_score
    
    def _check_password_rules(self, data):
        """Check password-related security rules"""
        if data.get('password_reuse') == 'yes':
            self._add_recommendation(
                'high',
                'Password Security',
                'Stop reusing passwords across accounts',
                'Use unique passwords for each account. Reused passwords put all your accounts at risk if one is compromised.',
                'Create unique passwords for each service immediately',
                20
            )
        
        if data.get('password_manager') == 'no':
            self._add_recommendation(
                'high',
                'Password Security',
                'Use a password manager',
                'Password managers like Bitwarden, 1Password, or LastPass help you create and store strong, unique passwords.',
                'Install and set up a reputable password manager',
                15
            )
    
    def _check_2fa_rules(self, data):
        """Check two-factor authentication rules"""
        if data.get('two_factor') == 'no':
            self._add_recommendation(
                'high',
                'Account Security',
                'Enable Two-Factor Authentication (2FA)',
                '2FA adds an extra layer of security. Enable it for email, banking, and social media accounts.',
                'Set up 2FA using authenticator apps (Google Authenticator, Authy) rather than SMS',
                20
            )
    
    def _check_network_rules(self, data):
        """Check network security rules"""
        if data.get('public_wifi') == 'yes' and data.get('vpn') == 'no':
            self._add_recommendation(
                'high',
                'Network Security',
                'Use VPN on public Wi-Fi networks',
                'Public Wi-Fi is vulnerable to interception. A VPN encrypts your connection.',
                'Install a trusted VPN service (Mullvad, ProtonVPN, or NordVPN)',
                18
            )
        
        if data.get('vpn') == 'no':
            self._add_recommendation(
                'medium',
                'Network Security',
                'Consider using a VPN for all internet activity',
                'VPNs protect your privacy by hiding your IP address and encrypting traffic.',
                'Research and subscribe to a reputable VPN service',
                12
            )
    
    def _check_device_rules(self, data):
        """Check device security rules"""
        if data.get('os_update') == 'no':
            self._add_recommendation(
                'high',
                'Device Security',
                'Keep your operating system and apps updated',
                'Updates patch security vulnerabilities. Enable automatic updates when possible.',
                'Check for and install all pending system and app updates now',
                15
            )
    
    def _check_privacy_rules(self, data):
        """Check privacy settings rules"""
        permissions = data.get('app_permissions', [])
        if len(permissions) > 2 and 'None' not in permissions:
            self._add_recommendation(
                'medium',
                'Privacy Settings',
                'Review and restrict app permissions',
                'Many apps request unnecessary permissions. Limit access to location, contacts, camera, and microphone.',
                'Go to Settings → Privacy and revoke unnecessary permissions',
                10
            )
    
    def _check_social_media_rules(self, data):
        """Check social media privacy rules"""
        social_media = data.get('social_media', [])
        if len(social_media) > 3:
            self._add_recommendation(
                'medium',
                'Social Media Privacy',
                'Review privacy settings on social media',
                'Limit who can see your posts, location, and personal information.',
                'Set profiles to private, disable location sharing, and review friend lists',
                8
            )
    
    def _check_backup_rules(self, data):
        """Check data backup rules"""
        if data.get('backup_data') == 'no':
            self._add_recommendation(
                'medium',
                'Data Protection',
                'Implement regular data backups',
                'Protect against data loss from ransomware, hardware failure, or theft.',
                'Set up automated backups using cloud services or external drives (3-2-1 backup rule)',
                10
            )
    
    def _check_encryption_rules(self, data):
        """Check email encryption rules"""
        if data.get('email_encryption') == 'no':
            self._add_recommendation(
                'low',
                'Communication Security',
                'Consider email encryption for sensitive communications',
                'For sensitive information, use encrypted email services or PGP encryption.',
                'Explore ProtonMail or Tutanota for encrypted email',
                5
            )
