# Smart Vet Care - AI Agent Instructions

## Project Overview
Smart Vet Care is a dual-model deep learning system for cattle disease and breed detection. The application combines a Streamlit web UI (`app.py`) with two independent TensorFlow/MobileNetV2 models trained on livestock imagery. This guide helps AI agents understand architectural patterns and development workflows specific to this project.

## Architecture

### Core Components
- **app.py**: Streamlit UI (main entry point) - handles image uploads and serves predictions from both models
- **breed_predict.py**: CLI tool for breed classification (5 cattle breeds)
- **disease_predict.py**: CLI tool for disease detection (FMD, Healthy, LSD)
- **Models**: Both use MobileNetV2 backbone (ImageNet pretrained, frozen), saved as `.keras` format (TF 2.x standard)

### Data Organization
```
datasets/
  ├─ breeds/ (raw images, folder names match class_names)
  └─ diseases/
training_data/
  ├─ breeds/ (train/val/test splits)
  └─ diseases/
processed_data/ (224x224 preprocessed images)
```

**Critical**: Dataset folder names must exactly match class labels in code (`Ayrshire_cattle`, `Brown_Swiss_cattle`, `Holstein_Friesian_cattle`, `Jersey_cattle`, `Red_Dane_cattle` for breeds; `FMD`, `Healthy`, `LSD` for diseases). The `flow_from_directory()` API derives class_indices from these folder names.

## Key Patterns & Conventions

### Model Architecture Pattern
Both training scripts follow identical pattern:
1. MobileNetV2 base (frozen weights)
2. GlobalAveragePooling2D
3. Dropout(0.4)
4. Dense softmax output layer
5. Adam optimizer (lr=1e-3), categorical_crossentropy loss

See [train_breed_model.py](train_breed_model.py#L49-L65) and [train_disease_model.py](train_disease_model.py#L62-L78).

### Image Preprocessing
- **Target size**: Always 224×224 (MobileNetV2 requirement)
- **Normalization**: Divide by 255.0 (implicit in app.py) or use `rescale=1./255` in ImageDataGenerator
- **Data augmentation**: Rotation (25°), zoom (0.2), shift, flip, brightness ([0.8, 1.2])

See [app.py](app.py#L62-L67) and [preprocess_images.py](preprocessing/preprocess_images.py#L36-L40).

### Model Loading Pattern
```python
# Standard pattern across all scripts
model = tf.keras.models.load_model("model_name.keras")
# Note: Some legacy code uses .h5, but .keras is the TF 2.x standard
```

### Class Label Consistency
When modifying class lists, update ALL of:
- Training script class folders
- [breed_predict.py](breed_predict.py#L16-L22) `class_names`
- [disease_predict.py](disease_predict.py#L13-L18) `class_names`  
- [app.py](app.py#L52-L60) `breed_classes` and `disease_classes`

Mismatch causes silent prediction errors (wrong indices returned).

### Class Imbalance Handling
Only disease model uses `compute_class_weight()` (line 51-56 in train_disease_model.py) due to FMD/LSD imbalance. Don't add to breed model unless data imbalance occurs.

## Development Workflows

### Training Models
```bash
# Breed classification (5 classes)
python train_breed_model.py

# Disease detection (3 classes, with class weights)
python train_disease_model.py
```
Outputs: `breed_model.keras`, `disease_model.keras` (cached in Streamlit)

### Testing Predictions via CLI
```bash
python breed_predict.py test_images/image.jpg
python disease_predict.py test_images/image.jpg
```

### Running the Web UI
```bash
streamlit run app.py
```
Models cached in memory via `@st.cache_resource` decorator. Streamlit reruns entire script on interaction—be cautious with expensive operations outside cache.

### Data Preparation
```bash
python preprocessing/preprocess_images.py  # Normalizes to 224×224
```
Utility scripts: `check_data.py`, `check_disease_data.py` (inspect dataset structure/counts).

## Critical Gotchas & Conventions

1. **Model format**: `.keras` files are TF 2.x standard (preferred over `.h5`). Both work with `load_model()`, but `.keras` is future-proof.

2. **Class ordering**: `flow_from_directory()` assigns indices alphabetically by folder name. Verify with `train_gen.class_indices` print statements during training.

3. **Image input shape**: Predictions expect `(1, 224, 224, 3)` after expand_dims. Forgetting the batch dimension causes shape mismatch errors.

4. **Streamlit caching**: Models cached via `@st.cache_resource`. Clearing cache requires browser refresh or `--logger.level=debug` rerun.

5. **TensorFlow suppression**: `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'` suppresses TF verbose logging. Preserve in production scripts.

## Common Tasks for AI Agents

- **Add new cattle breed**: Create folder in `datasets/breeds/`, update class_names in both scripts + app.py, retrain
- **Improve disease accuracy**: Collect more FMD/LSD samples (imbalance is primary bottleneck), tune class_weights, increase EPOCHS
- **Modify UI**: Edit [app.py](app.py) sections (menu logic is lines 75-176, predictions are lines 130-170)
- **Validate predictions**: Use `breed_predict.py` / `disease_predict.py` on test_images/ before deploying

## File Dependency Graph

```
app.py → breed_model.keras, disease_model.keras
breed_predict.py → breed_model.keras
disease_predict.py → disease_model.keras
train_breed_model.py → datasets/breeds/ → breed_model.keras
train_disease_model.py → datasets/diseases/ → disease_model.keras
preprocessing/preprocess_images.py → datasets/ → processed_data/
```

When modifying model architecture, both training and prediction scripts must align. Use print() statements to verify class_indices match.
