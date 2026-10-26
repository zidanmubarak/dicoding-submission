# Kriteria 2: Membangun Model Machine Learning

**Dataset**: Climate Change Impact on Agriculture 2024  
**Author**: Zidan Mubarak  
**Target Score**: Advanced (4 pts)

## Struktur Folder

```
Membangun_model/
├── modelling.py                          # Basic model dengan autolog (2 pts)
├── modelling_tuning.py                   # Advanced model dengan tuning (4 pts)
├── climate_change_preprocessing.csv      # Dataset preprocessing
├── screenshoot_dashboard.jpg             # Screenshot MLflow dashboard
├── screenshoot_artifak.jpg               # Screenshot MLflow artifacts
├── requirements.txt                      # Dependencies
├── DagsHub.txt                          # Link DagsHub MLflow
├── confusion_matrix.png                  # Artifact: Confusion matrix
├── feature_importance.png                # Artifact: Feature importance
├── roc_curve.png                        # Artifact: ROC curve
├── classification_report.txt             # Artifact: Classification report
└── README.md                            # Dokumentasi ini
```

## Kriteria yang Dipenuhi

1. **Model Training dengan MLflow**
   - ✓ Melatih model machine learning (Random Forest Classifier)
   - ✓ Menggunakan MLflow Tracking UI
   - ✓ Integrasi dengan DagsHub untuk tracking online

2. **Manual Logging (bukan autolog)**
   - ✓ Manual logging semua metrics
   - ✓ Metrics standard: accuracy, precision, recall, f1_score
   - ✓ Metrics tambahan (minimal 2):
     - ROC AUC Score
     - Train Accuracy
     - Cross-Validation Mean Score
     - Cross-Validation Std Score
     - Best CV Score
     - Overfitting Measure

3. **Hyperparameter Tuning**
   - ✓ GridSearchCV dengan parameter grid:
     - n_estimators: [100, 200, 300]
     - max_depth: [10, 15, 20, None]
     - min_samples_split: [2, 5, 10]
     - min_samples_leaf: [1, 2, 4]

4. **Artifacts Lengkap**
   - ✓ Model (saved via mlflow.sklearn.log_model)
   - ✓ Confusion Matrix (PNG)
   - ✓ Feature Importance (PNG)
   - ✓ ROC Curve (PNG) - Additional
   - ✓ Classification Report (TXT) - Additional

5. **DagsHub Integration**
   - ✓ MLflow tracking tersimpan di DagsHub
   - ✓ File DagsHub.txt berisi link repository

## Cara Menjalankan

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Setup MLflow Server (Lokal)

```bash
# Jalankan MLflow server di terminal terpisah
mlflow server --host 127.0.0.1 --port 5000
```

### 3. Setup DagsHub (Optional - untuk Advanced)

```bash
# Set environment variable dengan DagsHub token
$env:DAGSHUB_TOKEN="your_dagshub_token_here"

# Atau di Linux/Mac:
export DAGSHUB_TOKEN="your_dagshub_token_here"
```

**Cara mendapatkan DagsHub token:**
1. Login ke [DagsHub.com](https://dagshub.com)
2. Buat repository baru atau gunakan yang sudah ada
3. Pergi ke Settings > Tokens
4. Generate new token
5. Copy token dan set sebagai environment variable

### 4. Jalankan Model Training

#### Basic Model (2 pts)
```bash
python modelling.py
```

#### Advanced Model dengan Tuning (4 pts)
```bash
python modelling_tuning.py
```

### 5. Lihat Hasil di MLflow UI

- **Lokal**: http://127.0.0.1:5000
- **DagsHub**: https://dagshub.com/[username]/[repo-name].mlflow

## Model Details

### Dataset
- **Source**: climate_change_preprocessing.csv
- **Features**: Numeric features dari dataset climate change
- **Target**: Binary classification (High Yield vs Low Yield)
  - High Yield (1): Crop yield > median
  - Low Yield (0): Crop yield ≤ median

### Model
- **Algorithm**: Random Forest Classifier
- **Hyperparameter Tuning**: GridSearchCV dengan 5-fold cross-validation
- **Evaluation**: Train-test split (80-20) dengan stratified sampling

### Metrics Logged

#### Standard Metrics (seperti autolog)
- Test Accuracy
- Precision (weighted)
- Recall (weighted)
- F1 Score (weighted)

#### Additional Metrics (Advanced requirement)
- **ROC AUC Score**: Area under ROC curve
- **Train Accuracy**: Accuracy pada training set
- **CV Mean Score**: Mean cross-validation score
- **CV Std Score**: Standard deviation of CV scores
- **Best CV Score**: Best score dari GridSearchCV
- **Overfitting Measure**: Train accuracy - Test accuracy

### Artifacts Logged

1. **Model**: Trained Random Forest model
2. **Confusion Matrix**: Heatmap visualization
3. **Feature Importance**: Top 15 most important features
4. **ROC Curve**: ROC curve dengan AUC score
5. **Classification Report**: Detailed metrics per class
