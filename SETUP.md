# Development Setup Guide

This guide helps developers set up Smart Vet Care for local development.

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB+ recommended for model training)
- **Storage**: 3GB+ for datasets and models

## Step 1: Clone the Repository

```bash
git clone https://github.com/Anjally-200/SMART--VETCARE.git
cd SMART--VETCARE
```

## Step 2: Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Optional: Development Tools
```bash
pip install jupyter matplotlib ipython
```

## Step 4: Verify Installation

```bash
# Check Python
python --version

# Check TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"

# Check Streamlit
streamlit --version
```

## Step 5: Set Up Database (First Time Only)

```bash
python ai_consultation/database_setup.py
python create_db.py
```

## Step 6: Download/Prepare Models

If you don't have the pre-trained models:

```bash
# Train models (if needed)
python train_breed_model.py
python train_disease_model.py
```

Or download pre-trained models if available.

## Running the Application

### Launch Streamlit Web UI
```bash
streamlit run app.py
```
- Opens at `http://localhost:8501`
- Hot reload enabled for development

### Test Breed Prediction
```bash
python breed_predict.py path/to/image.jpg
```

### Test Disease Detection
```bash
python disease_predict.py path/to/image.jpg
```

## Project Structure Overview

```
SMART--VETCARE/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── SETUP.md                  # This file
│
├── Core Modules:
│   ├── breed_predict.py      # Breed classification
│   ├── disease_predict.py    # Disease detection
│   ├── auth.py               # User authentication
│   ├── farmer_dashboard.py   # Farmer interface
│   ├── vet_dashboard.py      # Veterinarian interface
│   └── admin_panel.py        # Admin interface
│
├── Training:
│   ├── train_breed_model.py
│   ├── train_disease_model.py
│   └── preprocessing/
│       └── preprocess_images.py
│
├── AI Engine:
│   └── ai_consultation/
│       ├── guidance_engine.py
│       └── database_setup.py
│
├── Models:
│   ├── breed_model.keras
│   └── disease_model.keras
│
└── Data:
    ├── datasets/             # Raw training data
    ├── training_data/        # Split train/val/test
    └── processed_data/       # Preprocessed images
```

## Common Development Tasks

### 1. Adding a New Feature

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Test changes
streamlit run app.py

# Commit and push
git add .
git commit -m "Add new feature: description"
git push origin feature/my-feature
```

### 2. Training a New Model

```bash
# Prepare data
python preprocessing/preprocess_images.py

# Train model
python train_breed_model.py
# or
python train_disease_model.py

# Model saved as breed_model.keras or disease_model.keras
```

### 3. Testing Predictions

```bash
# Individual predictions
python breed_predict.py test_image.jpg
python disease_predict.py test_image.jpg

# Or test within Streamlit
streamlit run app.py
# Upload image through web interface
```

### 4. Database Inspection

```bash
# Check database schema
python verify_db.py

# View database contents
sqlite3 consultations.db ".tables"
```

## IDE Setup Recommendations

### VS Code
1. Install extensions:
   - Python (Microsoft)
   - Pylance
   - Jupyter
   - Streamlit (optional)

2. Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

### PyCharm
1. Open project folder
2. Configure Python interpreter:
   - File → Settings → Project → Python Interpreter
   - Select your `venv` folder
3. Enable Django support (if needed for admin)

## Troubleshooting

### TensorFlow Issues
```bash
# Reinstall TensorFlow
pip install --upgrade tensorflow

# If GPU support needed
pip install tensorflow[and-cuda]
```

### Streamlit Issues
```bash
# Clear cache
streamlit run app.py --logger.level=debug

# Reinstall Streamlit
pip install --upgrade streamlit
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

### Model Not Found
```bash
# Check file exists
ls breed_model.keras
ls disease_model.keras

# Train if missing
python train_breed_model.py
python train_disease_model.py
```

## Performance Optimization

### For Development
- Use smaller datasets during testing
- Disable verbose logging: `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'`
- Cache models with `@st.cache_resource`

### For Production
- Use GPU acceleration if available
- Deploy on cloud (AWS, Google Cloud, Azure)
- Use Docker for containerization
- Set up monitoring and logging

## Code Quality

### Run Linter
```bash
flake8 app.py breed_predict.py disease_predict.py
```

### Check Style
```bash
pylint app.py
```

### Format Code
```bash
black app.py
```

## Useful Resources

- **TensorFlow**: https://www.tensorflow.org/
- **Streamlit**: https://docs.streamlit.io/
- **MobileNetV2**: https://keras.io/api/applications/mobilenet/#mobilenetv2
- **Python PEP 8**: https://pep8.org/

## Getting Help

- Check [README.md](README.md)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Search existing [Issues](https://github.com/Anjally-200/SMART--VETCARE/issues)
- Create a new Issue with details

---

**Happy Coding!**
