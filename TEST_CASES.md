# Test Cases & Examples for Knowledge Base Mapper

## 🧪 Comprehensive Test Suite

### Test Category 1: Password Security Questions (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "What password manager do you recommend?",
        "expected": True,
        "primary_topic": "Password Security",
        "explanation": "Asking about password managers"
    },
    {
        "prompt": "Is it bad to reuse passwords?",
        "expected": True,
        "primary_topic": "Password Security",
        "explanation": "Asking about password reuse"
    },
    {
        "prompt": "How do I create a strong password?",
        "expected": True,
        "primary_topic": "Password Security",
        "explanation": "Asking about password strength"
    },
    {
        "prompt": "Should I use Bitwarden or LastPass?",
        "expected": True,
        "primary_topic": "Password Security",
        "explanation": "Asking about specific password managers"
    },
    {
        "prompt": "What's a passphrase and is it more secure?",
        "expected": True,
        "primary_topic": "Password Security",
        "explanation": "Asking about passphrases"
    },
]
```

### Test Category 2: Account Security & 2FA (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "What is 2FA and how do I enable it?",
        "expected": True,
        "primary_topic": "Account Security",
        "explanation": "Asking about two-factor authentication"
    },
    {
        "prompt": "What's the difference between 2FA and MFA?",
        "expected": True,
        "primary_topic": "Account Security",
        "explanation": "Comparing authentication methods"
    },
    {
        "prompt": "Should I use Google Authenticator or Authy?",
        "expected": True,
        "primary_topic": "Account Security",
        "explanation": "Asking about authenticator apps"
    },
    {
        "prompt": "How do I recover my account if I lose my authenticator?",
        "expected": True,
        "primary_topic": "Account Security",
        "explanation": "Account recovery with backup codes"
    },
    {
        "prompt": "What are OTP codes?",
        "expected": True,
        "primary_topic": "Account Security",
        "explanation": "Asking about one-time passwords"
    },
]
```

### Test Category 3: Network Security & VPN (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "Should I use a VPN?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "Direct VPN question"
    },
    {
        "prompt": "Is it safe to connect to public Wi-Fi without VPN?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "Public Wi-Fi + VPN"
    },
    {
        "prompt": "What VPN services are trustworthy?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "VPN recommendations"
    },
    {
        "prompt": "Do I need DNS privacy protection?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "DNS privacy question"
    },
    {
        "prompt": "What about encrypted tunnels and proxies?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "Network encryption"
    },
]
```

### Test Category 4: Device Security (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "How often should I update my OS?",
        "expected": True,
        "primary_topic": "Device Security",
        "explanation": "Operating system updates"
    },
    {
        "prompt": "Are security patches important?",
        "expected": True,
        "primary_topic": "Device Security",
        "explanation": "Security patches"
    },
    {
        "prompt": "Do I need antivirus software?",
        "expected": True,
        "primary_topic": "Device Security",
        "explanation": "Antivirus software"
    },
    {
        "prompt": "Should I enable my firewall?",
        "expected": True,
        "primary_topic": "Device Security",
        "explanation": "Firewall configuration"
    },
    {
        "prompt": "How do I protect against malware?",
        "expected": True,
        "primary_topic": "Device Security",
        "explanation": "Malware protection"
    },
]
```

### Test Category 5: Privacy Settings (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "How do I restrict app permissions?",
        "expected": True,
        "primary_topic": "Privacy Settings",
        "explanation": "App permissions management"
    },
    {
        "prompt": "Should I allow location access?",
        "expected": True,
        "primary_topic": "Privacy Settings",
        "explanation": "Location sharing privacy"
    },
    {
        "prompt": "Can I disable camera and microphone access?",
        "expected": True,
        "primary_topic": "Privacy Settings",
        "explanation": "Camera/microphone permissions"
    },
    {
        "prompt": "How do I stop tracking?",
        "expected": True,
        "primary_topic": "Privacy Settings",
        "explanation": "Tracking prevention"
    },
    {
        "prompt": "What about data collection by apps?",
        "expected": True,
        "primary_topic": "Privacy Settings",
        "explanation": "Data collection control"
    },
]
```

### Test Category 6: Social Media Privacy (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "How do I make my Facebook private?",
        "expected": True,
        "primary_topic": "Social Media Privacy",
        "explanation": "Facebook privacy settings"
    },
    {
        "prompt": "Should I limit who sees my posts on Instagram?",
        "expected": True,
        "primary_topic": "Social Media Privacy",
        "explanation": "Instagram privacy"
    },
    {
        "prompt": "How do I manage my friend list?",
        "expected": True,
        "primary_topic": "Social Media Privacy",
        "explanation": "Friend list management"
    },
    {
        "prompt": "Can I stop my data from being exposed?",
        "expected": True,
        "primary_topic": "Social Media Privacy",
        "explanation": "Data exposure prevention"
    },
    {
        "prompt": "What about Twitter privacy settings?",
        "expected": True,
        "primary_topic": "Social Media Privacy",
        "explanation": "Twitter (X) privacy"
    },
]
```

### Test Category 7: Data Protection (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "How should I backup my data?",
        "expected": True,
        "primary_topic": "Data Protection",
        "explanation": "Data backups"
    },
    {
        "prompt": "What's ransomware and how do I protect against it?",
        "expected": True,
        "primary_topic": "Data Protection",
        "explanation": "Ransomware protection"
    },
    {
        "prompt": "What's the 3-2-1 backup rule?",
        "expected": True,
        "primary_topic": "Data Protection",
        "explanation": "Backup strategy"
    },
    {
        "prompt": "Should I use cloud backup?",
        "expected": True,
        "primary_topic": "Data Protection",
        "explanation": "Cloud backup options"
    },
    {
        "prompt": "How do I recover from data loss?",
        "expected": True,
        "primary_topic": "Data Protection",
        "explanation": "Data recovery"
    },
]
```

### Test Category 8: Communication Security (✅ Should Answer)

```python
test_cases = [
    {
        "prompt": "Should I encrypt my emails?",
        "expected": True,
        "primary_topic": "Communication Security",
        "explanation": "Email encryption"
    },
    {
        "prompt": "What's ProtonMail and how does it work?",
        "expected": True,
        "primary_topic": "Communication Security",
        "explanation": "Encrypted email service"
    },
    {
        "prompt": "What is PGP encryption?",
        "expected": True,
        "primary_topic": "Communication Security",
        "explanation": "PGP/GPG encryption"
    },
    {
        "prompt": "Are encrypted chat apps secure?",
        "expected": True,
        "primary_topic": "Communication Security",
        "explanation": "Secure messaging"
    },
    {
        "prompt": "What about end-to-end encryption?",
        "expected": True,
        "primary_topic": "Communication Security",
        "explanation": "E2E encryption"
    },
]
```

### Test Category 9: Out-of-Scope Questions (❌ Should NOT Answer)

```python
test_cases = [
    {
        "prompt": "What's 2 + 2?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Math question"
    },
    {
        "prompt": "What's the weather today?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Weather query"
    },
    {
        "prompt": "Tell me a joke",
        "expected": False,
        "primary_topic": None,
        "explanation": "Entertainment request"
    },
    {
        "prompt": "How do I bake a cake?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Cooking question"
    },
    {
        "prompt": "What's the capital of France?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Geography question"
    },
    {
        "prompt": "Tell me about quantum physics",
        "expected": False,
        "primary_topic": None,
        "explanation": "Science question"
    },
    {
        "prompt": "How do I fix my car?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Automotive question"
    },
    {
        "prompt": "What's your favorite movie?",
        "expected": False,
        "primary_topic": None,
        "explanation": "Entertainment preference"
    },
]
```

### Test Category 10: Edge Cases

```python
test_cases = [
    {
        "prompt": "",  # Empty string
        "expected": False,
        "primary_topic": None,
        "explanation": "Empty input"
    },
    {
        "prompt": "   ",  # Whitespace only
        "expected": False,
        "primary_topic": None,
        "explanation": "Whitespace input"
    },
    {
        "prompt": "password manager vpn 2fa backup encryption",
        "expected": True,
        "primary_topic": "Password Security",  # Most keywords here
        "explanation": "Multiple topics mixed"
    },
    {
        "prompt": "vpn vpn vpn",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "Repeated keywords"
    },
    {
        "prompt": "UPPERCASE VPN PASSWORD ENCRYPTION",
        "expected": True,
        "primary_topic": "Network Security",  # VPN has more keywords than password/encryption
        "explanation": "Case insensitivity"
    },
    {
        "prompt": "What about public-wifi and proxies?",
        "expected": True,
        "primary_topic": "Network Security",
        "explanation": "Hyphenated keywords"
    },
]
```

### Test Category 11: Multi-Topic Scenarios

```python
test_cases = [
    {
        "prompt": "How do I enable 2FA on my password manager account?",
        "expected": True,
        "primary_topic": "Account Security",  # or Password Security
        "related_topics": ["Account Security", "Password Security"],
        "explanation": "Both 2FA and password manager mentioned"
    },
    {
        "prompt": "Should I use a VPN and backup my data?",
        "expected": True,
        "primary_topic": "Network Security",  # or Data Protection
        "related_topics": ["Network Security", "Data Protection"],
        "explanation": "VPN and backup both mentioned"
    },
    {
        "prompt": "Encrypt my emails and enable 2FA",
        "expected": True,
        "primary_topic": "Communication Security",  # or Account Security
        "related_topics": ["Communication Security", "Account Security"],
        "explanation": "Email encryption and 2FA"
    },
    {
        "prompt": "Update my OS, restrict permissions, and use a VPN",
        "expected": True,
        "primary_topic": "Device Security",  # or others
        "related_topics": ["Device Security", "Privacy Settings", "Network Security"],
        "explanation": "Multiple privacy topics"
    },
]
```

---

## 🧬 Running Test Cases

### Method 1: Manual Testing
```python
from src.knowledge_base_mapper import KnowledgeBaseMapper

mapper = KnowledgeBaseMapper()

test_prompt = "How do I enable 2FA on my email?"
can_answer, topic, explanation = mapper.can_answer_question(test_prompt)

assert can_answer == True
assert topic == "Account Security"
print("✅ Test passed!")
```

### Method 2: Batch Testing
```python
def run_test_batch(test_cases):
    mapper = KnowledgeBaseMapper()
    passed = 0
    failed = 0
    
    for test in test_cases:
        can_answer, topic, _ = mapper.can_answer_question(test["prompt"])
        
        if can_answer == test["expected"]:
            if can_answer:
                if topic == test["primary_topic"]:
                    passed += 1
                    print(f"✅ {test['prompt'][:50]}...")
                else:
                    failed += 1
                    print(f"❌ {test['prompt'][:50]}... (wrong topic)")
            else:
                passed += 1
                print(f"✅ {test['prompt'][:50]}... (correctly rejected)")
        else:
            failed += 1
            print(f"❌ {test['prompt'][:50]}... (unexpected result)")
    
    print(f"\n{passed}/{len(test_cases)} tests passed")
    return passed, failed
```

### Method 3: Automated Test Suite
```bash
# Run comprehensive test suite
python test_knowledge_base_mapper.py

# Run specific test file
python -m pytest test_knowledge_base_mapper.py -v
```

---

## 📋 Test Results Template

```
┌─────────────────────────────────────────┐
│      Knowledge Base Mapper Test Results │
├─────────────────────────────────────────┤
│ Password Security:        8/8 ✅        │
│ Account Security:         5/5 ✅        │
│ Network Security:         5/5 ✅        │
│ Device Security:          5/5 ✅        │
│ Privacy Settings:         5/5 ✅        │
│ Social Media Privacy:     5/5 ✅        │
│ Data Protection:          5/5 ✅        │
│ Communication Security:   5/5 ✅        │
│ Out-of-Scope:            8/8 ✅        │
│ Edge Cases:              6/6 ✅        │
│ Multi-Topic:             4/4 ✅        │
├─────────────────────────────────────────┤
│ Total:                  66/66 ✅ 100%   │
└─────────────────────────────────────────┘
```

---

## 🎯 Regression Testing Checklist

Before each update:
- [ ] Run all 66 test cases
- [ ] Verify 100% pass rate
- [ ] Check new prompts don't break existing ones
- [ ] Test edge cases
- [ ] Validate multi-topic scenarios
- [ ] Document any new test cases added

---

**Test Version:** 1.0  
**Last Updated:** 2025  
**Coverage:** 100% of knowledge base topics
