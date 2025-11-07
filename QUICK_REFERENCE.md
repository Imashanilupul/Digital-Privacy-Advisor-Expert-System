# Quick Reference Guide - Knowledge Base Mapper

## 🚀 Quick Start

### Import the Mapper
```python
from src.knowledge_base_mapper import KnowledgeBaseMapper

# Create instance
mapper = KnowledgeBaseMapper()
```

### Check if Question is Answerable
```python
# Simple yes/no check
can_answer, primary_topic, explanation = mapper.can_answer_question(user_prompt)

if can_answer:
    print(f"Answer about {primary_topic}:\n{explanation}")
else:
    print(explanation)  # Shows why it's out of scope
```

### Get Detailed Mapping
```python
# Get complete mapping information
is_relevant, primary_topic, related_topics = mapper.check_prompt_relevance(user_prompt)

if is_relevant:
    print(f"Primary: {primary_topic}")
    print(f"Related: {related_topics}")
```

### Generate Explanation
```python
# Create user-facing explanation
explanation = mapper.generate_mapping_explanation(
    prompt, 
    primary_topic, 
    related_topics
)
print(explanation)
```

---

## 📚 Knowledge Base Topics

### 1️⃣ Password Security
**Keywords:** password, manager, reuse, unique, strong, Bitwarden, LastPass, 1Password, passphrase

**Covers:** Password creation, reuse issues, password managers, strong passwords

### 2️⃣ Account Security  
**Keywords:** 2fa, two-factor, authenticator, OTP, Google Authenticator, Authy, backup code

**Covers:** 2FA setup, multi-factor authentication, account recovery, backup codes

### 3️⃣ Network Security
**Keywords:** vpn, public wifi, encrypted connection, DNS, Mullvad, ProtonVPN, NordVPN

**Covers:** VPNs, public Wi-Fi safety, network encryption, DNS privacy

### 4️⃣ Device Security
**Keywords:** update, OS update, app update, antivirus, firewall, malware, patch

**Covers:** System updates, software patches, antivirus, device maintenance

### 5️⃣ Privacy Settings
**Keywords:** permission, location, camera, microphone, contacts, tracking, data collection

**Covers:** App permissions, tracking prevention, privacy controls, location sharing

### 6️⃣ Social Media Privacy
**Keywords:** social media, Facebook, Instagram, Twitter, profile, friend list, visibility

**Covers:** Profile privacy, sharing settings, friend lists, data exposure prevention

### 7️⃣ Data Protection
**Keywords:** backup, encryption, ransomware, data loss, encrypted, 3-2-1 backup

**Covers:** Data backups, encryption, ransomware protection, data loss prevention

### 8️⃣ Communication Security
**Keywords:** email, encryption, ProtonMail, Tutanota, PGP, GPG, encrypted chat

**Covers:** Email encryption, secure messaging, PGP/GPG, encrypted communications

---

## 🎯 Usage Examples

### Example 1: Check Single Question
```python
mapper = KnowledgeBaseMapper()

prompt = "How do I enable 2FA on my email account?"
can_answer, topic, explanation = mapper.can_answer_question(prompt)

# Output:
# can_answer: True
# topic: "Account Security"
# explanation: [formatted mapping info]
```

### Example 2: Handle Multiple Topics
```python
prompt = "Should I use a VPN and enable 2FA?"
is_relevant, primary, related = mapper.check_prompt_relevance(prompt)

# Output:
# is_relevant: True
# primary: "Network Security"  (more keywords matched)
# related: ["Network Security", "Account Security"]
```

### Example 3: Graceful Rejection
```python
prompt = "What's your favorite pizza topping?"
can_answer, topic, explanation = mapper.can_answer_question(prompt)

# Output:
# can_answer: False
# topic: None
# explanation: "[Formatted rejection message with available topics]"
```

### Example 4: Use in Streamlit
```python
import streamlit as st
from src.knowledge_base_mapper import KnowledgeBaseMapper

# Initialize
if "mapper" not in st.session_state:
    st.session_state.mapper = KnowledgeBaseMapper()

# Get user input
user_input = st.text_input("Ask about privacy...")

# Check relevance
if user_input:
    can_answer, topic, explanation = st.session_state.mapper.can_answer_question(user_input)
    
    if can_answer:
        st.success(f"✅ Can answer about: {topic}")
        # Call LLM to answer
    else:
        st.error(explanation)
```

---

## 🔧 Adding New Topics

### Step 1: Define the Topic
```python
# In src/knowledge_base_mapper.py, add to KNOWLEDGE_BASE:

"New Topic Name": {
    "keywords": [
        "keyword1",
        "keyword2", 
        "multi word phrase",
        # ... 10-15 keywords total
    ],
    "description": "Clear description of what this topic covers"
}
```

### Step 2: Test It
```python
mapper = KnowledgeBaseMapper()

# Test with related questions
test_prompts = [
    "Question about new topic?",
    "Another related question?"
]

for prompt in test_prompts:
    can_answer, topic, _ = mapper.can_answer_question(prompt)
    print(f"{prompt} → {topic if can_answer else 'OUT OF SCOPE'}")
```

### Step 3: Update Documentation
- Add topic to KNOWLEDGE_BASE_MAPPER.md
- Update this quick reference
- Add test cases to test_knowledge_base_mapper.py

---

## 🧪 Testing

### Run Full Test Suite
```bash
python test_knowledge_base_mapper.py
```

### Test Specific Question
```python
from src.knowledge_base_mapper import KnowledgeBaseMapper

mapper = KnowledgeBaseMapper()
can_answer, topic, explanation = mapper.can_answer_question("Your question here?")

print(f"Can answer: {can_answer}")
print(f"Topic: {topic}")
print(explanation)
```

### List All Topics
```python
mapper = KnowledgeBaseMapper()
for topic in mapper.get_all_topics():
    print(f"- {topic}")
    print(f"  {mapper.get_topic_description(topic)}\n")
```

---

## 📊 API Reference

### Methods

#### `check_prompt_relevance(prompt: str) → Tuple[bool, Optional[str], List[str]]`
**Returns:** (is_relevant, primary_topic, related_topics)
```python
is_relevant, primary, related = mapper.check_prompt_relevance("VPN question?")
```

#### `can_answer_question(prompt: str) → Tuple[bool, Optional[str], str]`
**Returns:** (can_answer, primary_topic, explanation)
```python
can_answer, topic, msg = mapper.can_answer_question("2FA question?")
```

#### `get_topic_description(topic: str) → Optional[str]`
**Returns:** Description string or None
```python
desc = mapper.get_topic_description("Password Security")
```

#### `get_all_topics() → List[str]`
**Returns:** List of all topic names
```python
all_topics = mapper.get_all_topics()
```

#### `generate_mapping_explanation(...) → str`
**Returns:** Formatted explanation
```python
explanation = mapper.generate_mapping_explanation(prompt, primary, related)
```

---

## 🎓 Integration Checklist

- [ ] Import `KnowledgeBaseMapper` in your module
- [ ] Initialize mapper in session state
- [ ] Call `can_answer_question()` before LLM response
- [ ] Handle True case: answer with context
- [ ] Handle False case: show explanation
- [ ] Display mapping info to user
- [ ] Test with various prompts
- [ ] Monitor for edge cases

---

## 💡 Best Practices

### ✅ DO
- Use `can_answer_question()` for simple yes/no
- Show mapping explanation to users
- Test with realistic user prompts
- Keep keywords specific and distinct
- Document new topics when added

### ❌ DON'T
- Skip the relevance check
- Answer out-of-scope questions
- Make keywords too generic
- Remove established topics
- Modify keywords without testing

---

## 🐛 Troubleshooting

### Question marked as out-of-scope but should be in-scope
1. Check if keywords are included in the topic
2. Verify keyword spelling/variations
3. Add missing keywords to the topic
4. Re-test the question

### Question marked as in-scope but shouldn't be
1. Check if keywords are too generic
2. Review keyword combinations
3. Consider removing ambiguous keywords
4. Add more specific alternatives

### Unexpected primary topic
1. Check keyword counts for each matched topic
2. Topic with most keyword matches wins
3. Add more specific keywords to correct topic
4. Remove overlapping keywords if needed

---

## 📞 Support

For issues or questions:
1. Check KNOWLEDGE_BASE_MAPPER.md for detailed docs
2. Review test_knowledge_base_mapper.py for examples
3. Check IMPLEMENTATION_SUMMARY.md for architecture
4. Run test suite to verify functionality

---

**Version:** 1.0  
**Last Updated:** 2025  
**Status:** ✅ Production Ready
