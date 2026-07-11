# Smart Vet Care 🐄

**AI-Powered Cattle Disease & Breed Detection System**

A comprehensive deep learning solution for automated cattle health monitoring and breed identification using TensorFlow/Keras and Streamlit.

---

## 📋 Features

✅ **Dual Model Architecture**
- **Breed Classification**: Identifies 5 cattle breeds (Ayrshire, Brown Swiss, Holstein Friesian, Jersey, Red Dane)
- **Disease Detection**: Detects livestock diseases (FMD, LSD, Healthy)

✅ **Web Interface** 
- Streamlit-based web application for easy image uploads and predictions
- Real-time inference with pre-trained models

✅ **User Roles**
- **Admin Panel**: System configuration and data management
- **Veterinarian Dashboard**: Clinical assessment tools
- **Farmer Dashboard**: Livestock monitoring and health reports
- **Authentication**: Secure login system for all user types

✅ **AI Consultation Engine**
- Breed history tracking
- Disease history management  
- Guidance recommendations based on predictions

✅ **Multi-User Support**
- User authentication and authorization
- Role-based access control
- Consultation messaging system

---

## 🏗️ Project Structure

```
smart-vet-care/
├── app.py                          # Main Streamlit application
├── breed_predict.py                # Breed classification CLI/module
├── disease_predict.py              # Disease detection CLI/module
├── train_breed_model.py            # Breed model training script
├── train_disease_model.py          # Disease model training script
├── breed_model.keras               # Pre-trained breed model
├── disease_model.keras             # Pre-trained disease model
│
├── auth.py                         # Authentication module
├── admin_panel.py                  # Admin dashboard
├── farmer_dashboard.py             # Farmer interface
├── vet_dashboard.py                # Veterinarian interface
├── doctor_login.py                 # Vet login handler
├── admin_login.py                  # Admin login handler
│
├── ai_consultation/                # AI consultation engine
│   ├── guidance_engine.py
│   ├── create_breed_history.py
│   ├── create_disease_history.py
│   └── database_setup.py
│
├── datasets/                       # Training datasets
│   ├── breeds/
│   │   ├── Ayrshire_cattle/
│   │   ├── Brown_Swiss_cattle/
│   │   ├── Holstein_Friesian_cattle/
│   │   ├── Jersey_cattle/
│   │   └── Red_Dane_cattle/
│   └── diseases/
│       ├── FMD/
│       ├── Healthy/
│       └── LSD/
│
├── training_data/                  # Processed training/validation splits
│   ├── breeds/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── diseases/
│       ├── train/
│       ├── val/
│       └── test/
│
├── preprocessing/                  # Data preprocessing utilities
│   └── preprocess_images.py
│
└── requirements.txt               # Python dependencies
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- 2GB+ RAM (for model inference)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Anjally-200/SMART--VETCARE.git
cd SMART--VETCARE
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

**Start the Streamlit web application:**
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

**Use prediction CLI tools:**
```bash
# Breed prediction
python breed_predict.py path/to/cattle_image.jpg

# Disease prediction
python disease_predict.py path/to/cattle_image.jpg
```

---

## 🎯 Model Architecture

Both models use **MobileNetV2** with ImageNet pre-trained weights:

```
Input (224×224×3)
    ↓
MobileNetV2 Base (frozen weights)
    ↓
GlobalAveragePooling2D
    ↓
Dropout(0.4)
    ↓
Dense(softmax) - Output Layer
```

**Training Configuration:**
- Optimizer: Adam (lr=0.001)
- Loss: Categorical Crossentropy
- Batch Size: 16
- Image Size: 224×224 pixels
- Epochs: 20

---

## 📊 Data Preparation

### Dataset Organization
```
datasets/breeds/
├── Ayrshire_cattle/           [Folder names = Class labels]
├── Brown_Swiss_cattle/
├── Holstein_Friesian_cattle/
├── Jersey_cattle/
└── Red_Dane_cattle/

datasets/diseases/
├── FMD/
├── Healthy/
└── LSD/
```

### Image Preprocessing
- Resize: 224×224 pixels (MobileNetV2 requirement)
- Normalization: Rescale by 1/255.0
- Augmentation: Rotation, zoom, shift, flip, brightness adjustment

**Prepare data:**
```bash
python preprocessing/preprocess_images.py
```

---

## 🔐 User Authentication

The system supports three user roles:

| Role | Capabilities |
|------|--------------|
| **Admin** | System configuration, user management, data oversight |
| **Veterinarian** | Clinical predictions, consultation management, reports |
| **Farmer** | Livestock monitoring, health checks, consultation requests |

Default admin account setup:
```bash
python create_admin.py
```

---

## 🧠 AI Consultation Engine

The `ai_consultation/` module provides:
- **Breed History**: Track breed identification history per animal
- **Disease History**: Maintain disease detection records
- **Guidance Engine**: Generate recommendations based on prediction confidence and historical data
- **Database**: SQLite-based persistence for all records

Initialize consultation database:
```bash
python ai_consultation/database_setup.py
```

---

## 📈 Performance Metrics

- **Breed Model Accuracy**: Optimized for high precision
- **Disease Model Accuracy**: Class-weighted training to handle imbalance
- **Inference Speed**: <500ms per image (CPU)

---

## 🔧 Development & Training

### Training New Models

**Train breed model:**
```bash
python train_breed_model.py
```
Output: `breed_model.keras`

**Train disease model:**
```bash
python train_disease_model.py
```
Output: `disease_model.keras`

### Data Validation
```bash
python check_data.py          # Validate breed dataset
python check_disease_data.py  # Validate disease dataset
```

---

## 📝 Key Implementation Notes

1. **Class Label Consistency**: Folder names in datasets must exactly match class labels in code (e.g., `Ayrshire_cattle`)
2. **Model Format**: Uses `.keras` format (TF 2.x standard) instead of `.h5`
3. **Image Input**: Predictions expect (1, 224, 224, 3) shape after batch expansion
4. **Streamlit Caching**: Models cached via `@st.cache_resource` for fast loading

---

## 🐛 Troubleshooting

**Model not found error:**
- Ensure `breed_model.keras` and `disease_model.keras` are in the project root
- Run training scripts if models don't exist

**Shape mismatch in predictions:**
- Verify input images are resized to 224×224
- Check batch dimension is added: `image = np.expand_dims(image, axis=0)`

**Class name mismatch:**
- Ensure dataset folder names match `class_names` lists in prediction scripts
- Update all three locations if changing class labels

**Database errors:**
- Run `python create_db.py` to initialize database schema
- Check file permissions in the project directory

---

## 📦 Dependencies

Key packages (see `requirements.txt` for complete list):
- **TensorFlow 2.x**: Deep learning framework
- **Streamlit**: Web application framework
- **NumPy**: Numerical computing
- **Pillow**: Image processing
- **SQLite3**: Database management

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Smart Vet Care Development Team**

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an GitHub Issue
- Contact: Anjally-200 on GitHub

---

## 🙏 Acknowledgments

- TensorFlow/Keras team for deep learning framework
- Streamlit team for web app framework
- MobileNetV2 architecture (Howard et al., 2018)
- Livestock disease research community

---

**Last Updated**: July 2026  
**Version**: 1.0.0
