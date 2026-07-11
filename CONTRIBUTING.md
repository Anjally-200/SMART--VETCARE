# Contributing to Smart Vet Care

Thank you for your interest in contributing to Smart Vet Care! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/SMART--VETCARE.git
   cd SMART--VETCARE
   ```

3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Install development dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pylint flake8
   ```

## Development Workflow

1. **Make your changes** following the code style guidelines below
2. **Test your changes** thoroughly
3. **Commit** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: brief description of changes"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** with a clear title and description

## Code Style Guidelines

### Python Style
- Follow **PEP 8** standards
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters (where practical)

### Example Function:
```python
def predict_breed(image_path: str) -> dict:
    """
    Predict cattle breed from image.
    
    Args:
        image_path: Path to the cattle image file
        
    Returns:
        Dictionary with breed prediction and confidence score
    """
    # Implementation here
    return {
        'breed': breed_name,
        'confidence': confidence_score
    }
```

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Prefix private functions/variables with `_`

## Testing

Before submitting a pull request:

1. **Test your code locally:**
   ```bash
   python -m pytest tests/
   ```

2. **Check for syntax errors:**
   ```bash
   flake8 your_modified_file.py
   ```

3. **Manual testing** (especially for ML models):
   - Test with various image inputs
   - Verify predictions are reasonable
   - Check error handling

## Types of Contributions

### Bug Reports
- Check existing issues first to avoid duplicates
- Provide:
  - Clear description of the bug
  - Steps to reproduce
  - Expected vs. actual behavior
  - System information (OS, Python version, etc.)

### Feature Requests
- Describe the feature clearly
- Explain the use case and benefits
- Provide examples if possible

### Code Improvements
- Performance optimizations
- Code refactoring
- Documentation improvements
- Model improvements with metrics

## Model Training & Evaluation

If contributing model improvements:

1. **Document dataset changes:**
   - New classes or breeds
   - Dataset size changes
   - Data augmentation modifications

2. **Report metrics:**
   - Accuracy on test set
   - Precision, recall, F1-score per class
   - Training time and computational requirements
   - Inference time

3. **Save models properly:**
   - Use `.keras` format (TF 2.x standard)
   - Include model architecture diagram
   - Document any hyperparameter changes

## Documentation

- Update `README.md` if adding features
- Add docstrings to all new functions
- Update this file if adding new guidelines
- Keep documentation clear and concise

## Commit Messages

Use clear, descriptive commit messages:

```
Good:
  "Fix breed prediction accuracy by updating training data normalization"
  "Add disease history tracking feature"
  "Improve model loading performance with caching"

Avoid:
  "Fix bug"
  "Update code"
  "Changes"
```

## Pull Request Process

1. Update documentation and README as needed
2. Add any new dependencies to `requirements.txt`
3. Ensure code passes linting checks
4. Provide clear description of changes
5. Link to related issues if applicable
6. Be responsive to review feedback

## Areas We Need Help With

- 🎨 **UI/UX Improvements**: Streamlit interface enhancements
- 📊 **Model Improvements**: Better accuracy, faster inference
- 📚 **Documentation**: Tutorials, guides, video explanations
- 🧪 **Testing**: Unit tests, integration tests
- 🔒 **Security**: Authentication improvements, data protection
- 🌍 **Localization**: Multi-language support

## Questions?

Feel free to:
- Open an issue with your question
- Comment on related issues/PRs
- Contact the maintainers

---

**Thank you for contributing to Smart Vet Care! 🐄**
