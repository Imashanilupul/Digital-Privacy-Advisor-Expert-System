; Sample user profile for testing

(assert (user-profile
   (user-id "test-user-001")
   (social-media Facebook Instagram Twitter TikTok)
   (devices Smartphone Laptop Tablet)
   (password-reuse yes)
   (password-manager no)
   (two-factor no)
   (public-wifi yes)
   (vpn no)
   (os-update no)
   (app-permissions Location Contacts Camera Microphone)
   (backup-data no)
   (email-encryption no)))

(run)