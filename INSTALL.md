
# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Quick Start (Windows)

### 1. Clone the repository
```bash
git clone https://github.com/Imashanilupul/Digital-Privacy-Advisor-Expert-System.git
cd Digital-Privacy-Advisor-Expert-System
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Upgrade pip and install dependencies
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

### 4. Verify installation
```bash
python -c "import streamlit, google.generativeai, pytest; print('✓ All packages installed')"
```

## Troubleshooting

### Issue: `ResolutionImpossible` dependency conflict

**Solution**: Use version ranges instead of pinned versions:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

If that fails, install individually:
```bash
pip install streamlit --no-cache-dir
pip install google-generativeai --no-cache-dir
pip install pytest --no-cache-dir
pip install clipspy --no-cache-dir
```

### Issue: Module not found after installation

**Solution**: Ensure your virtual environment is activated:
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

Then verify with:
```bash
pip list
```

### Issue: Streamlit won't start

**Solution**: Ensure all dependencies loaded correctly:
```bash
pip install streamlit==1.51.0 --force-reinstall --no-cache-dir
```

### Issue: Google Gemini API errors

**Solution**: Ensure `google-generativeai` is installed:
```bash
pip install google-generativeai --upgrade --no-cache-dir
```

## Running the application

After successful installation:

```bash
streamlit run app.py
```

Then open browser to: `http://localhost:8501`

## Alternative: Docker

If you have Docker installed, build and run without installing locally:

```bash
docker build -t privacy-advisor .
docker run -p 8501:8501 privacy-advisor
```

## Uninstall

To remove the project:
```bash
deactivate
cd ..
rm -r Digital-Privacy-Advisor-Expert-System
```

## Support

For issues, check:
- [Streamlit Docs](https://docs.streamlit.io)
- [Google Generative AI Docs](https://ai.google.dev/docs)
- [Project Issues](https://github.com/Imashanilupul/Digital-Privacy-Advisor-Expert-System/issues)
