# Quick Reference: AI Issue Analysis

## The New System in 30 Seconds

**Old System**: Answer 10+ predefined questions
**New System**: Describe your concern → AI analyzes → Get personalized report

## 4-Step Flow

```
You Type → AI Classifies → You Clarify → AI Recommends
   Issue      the Issue    with Q&A        Solutions
```

## Getting Started

1. **Get API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Run App**: `streamlit run app.py`
3. **Paste Key**: In sidebar when prompted
4. **Describe Issue**: "I reuse passwords" or "I use public WiFi"
5. **Answer Questions**: 4-5 tailored follow-ups
6. **Read Report**: Get detailed analysis

## Privacy Categories

| 🔐 | Password | 👤 | Accounts | 🌐 | Network | 💻 | Devices |
|----|----------|----|---------| ----|---------|-----|---------|
| 📁 | Data     | 📧 | Email   | ⚙️ | Privacy | 📱 | Social  |

## Example Issues

### "I reuse passwords"
```
Category: 🔐 Password Security
Severity: 🔴 HIGH (Risk: 78/100)
Follow-up: How many accounts? Use 2FA?
Result: Change critical passwords, get password manager
```

### "Public WiFi for banking"
```
Category: 🌐 Network Security
Severity: 🔴 CRITICAL (Risk: 90/100)
Follow-up: How often? Have you been hacked?
Result: Use VPN, enable 2FA, avoid public WiFi
```

### "Don't back up files"
```
Category: 📁 Data Protection
Severity: 🟡 MEDIUM (Risk: 65/100)
Follow-up: What data? Cloud or external drive?
Result: Set up automatic backups, use encryption
```

## Report Sections

| Section | Contains |
|---------|----------|
| 📋 Analysis | What's wrong and why |
| 🔍 Root Causes | What caused the issue |
| 🚨 Immediate | Do this NOW (High priority) |
| ⏱️ Medium-term | Do this soon (Regular priority) |
| 🛠️ Tools | Specific products to use |
| ⏳ Timeline | When to do each step |
| ❓ FAQ | Q&A about solutions |

## Key Features

✅ Natural language input (your own words)
✅ AI-powered analysis (Gemini)
✅ Personalized questions
✅ Detailed explanations
✅ Actionable steps
✅ Tool recommendations
✅ Implementation timeline

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "API key error" | Get new key from Google AI Studio |
| "No response" | Check internet, verify API key |
| "Vague questions" | Describe your issue more specifically |
| "Report incomplete" | Some sections only appear for certain issues |

## File Locations

```
app.py                          Main Streamlit application
src/issue_classifier.py         AI classification engine
AI_ISSUE_ANALYSIS_GUIDE.md      Full documentation
QUICK_REFERENCE.md              This file
```

## Code Example

```python
from src.issue_classifier import IssueClassifier

# Initialize
classifier = IssueClassifier(api_key="your_key")

# Step 1: Classify
classification = classifier.classify_issue(
    "I reuse passwords everywhere"
)
print(classification['severity'])  # "high"

# Step 2: Get follow-ups
questions = classifier.generate_followup_questions(classification)
print(len(questions))  # 4-5 questions

# Step 3: Generate report
report = classifier.generate_report({
    "user_issue": "...",
    "classification": classification,
    "followup_answers": {"q1": "Yes", "q2": "5 accounts"}
})
print(report['immediate_actions'])  # [{"action": "...", "why": "..."}]
```

## API Limits

- **Model**: gemini-2.5-flash
- **Rate**: 15 requests per minute (free tier)
- **Tokens**: ~32K input, ~8K output per request
- **Cost**: FREE for reasonable use

## Icons Guide

| Icon | Meaning | Icon | Meaning |
|------|---------|------|---------|
| 🟢 | Low risk/priority | 🔴 | High risk/immediate |
| 🟡 | Medium risk | 🟠 | Medium-high |
| ✅ | Complete/configure | ⏳ | Do over time |
| 🚨 | Urgent | 💡 | Helpful tip |

## Before You Start

✓ Have Gemini API key ready
✓ Describe your issue clearly
✓ Be specific (not "privacy worried" but "I reuse passwords")
✓ Answer follow-up questions honestly
✓ Have time to implement recommendations (30 min - 2 hours)

## After Analysis

1. **Read the report carefully** - All recommendations are personalized
2. **Start with 🔴 actions** - Do urgent items first
3. **Use recommended tools** - They're tested and proven
4. **Follow the timeline** - Realistic schedule for changes
5. **Reference FAQ** - Answers common implementation questions

## More Help

- Full guide: `AI_ISSUE_ANALYSIS_GUIDE.md`
- Code docs: Comments in `src/issue_classifier.py`
- Examples: See Readme.md for sample scenarios
- Issues: File bug reports in GitHub issues
