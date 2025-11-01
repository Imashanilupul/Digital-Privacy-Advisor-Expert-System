; Digital Privacy Advisor - Fact Templates
; Defines the structure of user input facts

(deftemplate user-profile
   (slot user-id)
   (multislot social-media)
   (multislot devices)
   (slot password-reuse)
   (slot password-manager)
   (slot two-factor)
   (slot public-wifi)
   (slot vpn)
   (slot os-update)
   (multislot app-permissions)
   (slot backup-data)
   (slot email-encryption))

(deftemplate recommendation
   (slot priority)
   (slot category)
   (slot message)
   (slot details)
   (slot action)
   (slot risk-score))