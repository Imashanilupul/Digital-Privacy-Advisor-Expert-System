; Digital Privacy Advisor - Knowledge Base Rules
; Contains all security assessment rules

; Load templates first
(load "clips/templates.clp")

; Password Security Rules
(defrule password-reuse-rule
   (user-profile (password-reuse yes))
   =>
   (assert (recommendation
      (priority high)
      (category "Password Security")
      (message "Stop reusing passwords across accounts")
      (details "Use unique passwords for each account. Reused passwords put all your accounts at risk if one is compromised.")
      (action "Create unique passwords for each service immediately")
      (risk-score 20))))

(defrule no-password-manager-rule
   (user-profile (password-manager no))
   =>
   (assert (recommendation
      (priority high)
      (category "Password Security")
      (message "Use a password manager")
      (details "Password managers like Bitwarden, 1Password, or LastPass help you create and store strong, unique passwords.")
      (action "Install and set up a reputable password manager")
      (risk-score 15))))

; Two-Factor Authentication Rules
(defrule no-two-factor-rule
   (user-profile (two-factor no))
   =>
   (assert (recommendation
      (priority high)
      (category "Account Security")
      (message "Enable Two-Factor Authentication (2FA)")
      (details "2FA adds an extra layer of security. Enable it for email, banking, and social media accounts.")
      (action "Set up 2FA using authenticator apps (Google Authenticator, Authy) rather than SMS")
      (risk-score 20))))

; Network Security Rules
(defrule public-wifi-no-vpn-rule
   (user-profile (public-wifi yes) (vpn no))
   =>
   (assert (recommendation
      (priority high)
      (category "Network Security")
      (message "Use VPN on public Wi-Fi networks")
      (details "Public Wi-Fi is vulnerable to interception. A VPN encrypts your connection.")
      (action "Install a trusted VPN service (Mullvad, ProtonVPN, or NordVPN)")
      (risk-score 18))))

(defrule no-vpn-rule
   (user-profile (vpn no))
   =>
   (assert (recommendation
      (priority medium)
      (category "Network Security")
      (message "Consider using a VPN for all internet activity")
      (details "VPNs protect your privacy by hiding your IP address and encrypting traffic.")
      (action "Research and subscribe to a reputable VPN service")
      (risk-score 12))))

; Device Security Rules
(defrule no-os-update-rule
   (user-profile (os-update no))
   =>
   (assert (recommendation
      (priority high)
      (category "Device Security")
      (message "Keep your operating system and apps updated")
      (details "Updates patch security vulnerabilities. Enable automatic updates when possible.")
      (action "Check for and install all pending system and app updates now")
      (risk-score 15))))

; Privacy Settings Rules
(defrule excessive-permissions-rule
   (user-profile (app-permissions $?perms&:(> (length$ ?perms) 2)))
   =>
   (assert (recommendation
      (priority medium)
      (category "Privacy Settings")
      (message "Review and restrict app permissions")
      (details "Many apps request unnecessary permissions. Limit access to location, contacts, camera, and microphone.")
      (action "Go to Settings -> Privacy and revoke unnecessary permissions")
      (risk-score 10))))

; Social Media Rules
(defrule many-social-media-rule
   (user-profile (social-media $?sm&:(> (length$ ?sm) 3)))
   =>
   (assert (recommendation
      (priority medium)
      (category "Social Media Privacy")
      (message "Review privacy settings on social media")
      (details "Limit who can see your posts, location, and personal information.")
      (action "Set profiles to private, disable location sharing, and review friend lists")
      (risk-score 8))))

; Data Protection Rules
(defrule no-backup-rule
   (user-profile (backup-data no))
   =>
   (assert (recommendation
      (priority medium)
      (category "Data Protection")
      (message "Implement regular data backups")
      (details "Protect against data loss from ransomware, hardware failure, or theft.")
      (action "Set up automated backups using cloud services or external drives (3-2-1 backup rule)")
      (risk-score 10))))

; Email Encryption Rules
(defrule no-email-encryption-rule
   (user-profile (email-encryption no))
   =>
   (assert (recommendation
      (priority low)
      (category "Communication Security")
      (message "Consider email encryption for sensitive communications")
      (details "For sensitive information, use encrypted email services or PGP encryption.")
      (action "Explore ProtonMail or Tutanota for encrypted email")
      (risk-score 5))))