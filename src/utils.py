"""
Utility functions for the Digital Privacy Advisor
"""

def calculate_risk_level(risk_score):
    """
    Calculate risk level based on total risk score
    
    Args:
        risk_score (int): Total accumulated risk score
        
    Returns:
        str: Risk level (Low, Medium, High, Critical)
    """
    if risk_score >= 50:
        return "Critical"
    elif risk_score >= 30:
        return "High"
    elif risk_score >= 15:
        return "Medium"
    else:
        return "Low"

def get_risk_color(risk_level):
    """
    Get color code for risk level
    
    Args:
        risk_level (str): Risk level
        
    Returns:
        str: Hex color code
    """
    colors = {
        "Critical": "#dc2626",
        "High": "#ea580c",
        "Medium": "#ca8a04",
        "Low": "#16a34a"
    }
    return colors.get(risk_level, "#6b7280")

def format_report(user_data, recommendations, risk_level, risk_score):
    """
    Format assessment report for export
    
    Args:
        user_data (dict): User input data
        recommendations (list): List of recommendations
        risk_level (str): Calculated risk level
        risk_score (int): Total risk score
        
    Returns:
        str: Formatted report text
    """
    from datetime import datetime
    
    report = f"""
DIGITAL PRIVACY ASSESSMENT REPORT
{'='*70}
Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Risk Level: {risk_level} (Score: {risk_score})

USER PROFILE SUMMARY
{'-'*70}
Social Media Platforms: {', '.join(user_data.get('social_media', [])) or 'None'}
Devices Used: {', '.join(user_data.get('devices', [])) or 'None'}
Password Manager: {user_data.get('password_manager', 'Unknown')}
Two-Factor Authentication: {user_data.get('two_factor', 'Unknown')}
VPN Usage: {user_data.get('vpn', 'Unknown')}
Regular OS Updates: {user_data.get('os_update', 'Unknown')}
Data Backup: {user_data.get('backup_data', 'Unknown')}

RECOMMENDATIONS ({len(recommendations)} total)
{'-'*70}
"""
    
    for idx, rec in enumerate(recommendations, 1):
        report += f"""
{idx}. [{rec['priority'].upper()}] {rec['category']}
   {rec['message']}
   
   Details: {rec['details']}
   
   Action: {rec['action']}
   
"""
    
    report += f"""
{'='*70}
NEXT STEPS
{'-'*70}
1. Address high-priority items first
2. Implement recommendations gradually over 30 days
3. Re-assess your security quarterly
4. Stay informed about emerging threats
5. Share this tool with family and friends

For more information on digital privacy and security, visit:
- Electronic Frontier Foundation (EFF): https://www.eff.org
- Privacy Guides: https://www.privacyguides.org
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
"""
    
    return report

def sort_recommendations(recommendations):
    """
    Sort recommendations by priority
    
    Args:
        recommendations (list): List of recommendation dicts
        
    Returns:
        list: Sorted recommendations
    """
    priority_order = {"high": 1, "medium": 2, "low": 3}
    return sorted(recommendations, key=lambda x: priority_order.get(x['priority'], 999))
