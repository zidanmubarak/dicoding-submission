"""
Kriteria 2: Membangun Model Machine Learning
Dataset: Climate Change Impact on Agriculture 2024
Author: Zidan Mubarak
Description: Advanced model training with:
- Hyperparameter tuning
- Manual logging (not autolog)
- Additional metrics beyond autolog
- DagsHub integration
- Additional artifacts
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Try to import dagshub
try:
    import dagshub
    DAGSHUB_AVAILABLE = True
except ImportError:
    DAGSHUB_AVAILABLE = False
    print("⚠️ dagshub library not installed. Install with: pip install dagshub")

def setup_mlflow_tracking(use_dagshub=False):
    """
    Setup MLflow tracking URI
    
    Parameters:
    -----------
    use_dagshub : bool
        Whether to use DagsHub for remote tracking
    """
    if use_dagshub and DAGSHUB_AVAILABLE:
        print("\n" + "="*70)
        print("DAGSHUB SETUP")
        print("="*70)
        
        # DagsHub repository configuration
        dagshub_owner = "zidanmubarak"  
        dagshub_repo = "Eksperimen_SML_Zidan-Mubarak"  
        
        print(f"\n📌 DagsHub Configuration:")
        print(f"   Owner: {dagshub_owner}")
        print(f"   Repository: {dagshub_repo}")
        print(f"   URL: https://dagshub.com/{dagshub_owner}/{dagshub_repo}")
        
        print("\n⚠️ PENTING: Pastikan repository sudah dibuat di DagsHub!")
        print("   1. Login ke https://dagshub.com")
        print("   2. Klik 'Create Repository' atau gunakan yang sudah ada")
        print("   3. Nama repository harus sama dengan konfigurasi di atas")
        
        try:
            # Initialize DagsHub
            dagshub.init(
                repo_owner=dagshub_owner,
                repo_name=dagshub_repo,
                mlflow=True
            )
            print(f"\n✅ DagsHub initialized successfully!")
            print(f"   MLflow Tracking: https://dagshub.com/{dagshub_owner}/{dagshub_repo}.mlflow")
            return f"https://dagshub.com/{dagshub_owner}/{dagshub_repo}.mlflow"
            
        except Exception as e:
            print(f"\n❌ Error initializing DagsHub: {str(e)}")
            print("   Falling back to local MLflow...")
            mlflow.set_tracking_uri("http://127.0.0.1:5000")
            return "http://127.0.0.1:5000"
    else:
        # Use local MLflow
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        print("\n✅ Using local MLflow tracking: http://127.0.0.1:5000")
        return "http://127.0.0.1:5000"

def load_and_prepare_data():
    """Load and prepare the preprocessed dataset"""
    print("\n📂 Loading preprocessed dataset...")
    df = pd.read_csv('climate_change_preprocessing.csv')
    
    print(f"Dataset shape: {df.shape}")
    
    # Define features (exclude target and non-numeric columns)
    exclude_cols = ['Crop_Yield_MT_per_HA', 'Country', 'Region', 'Crop_Type', 'Unnamed: 0']
    feature_cols = [col for col in df.columns if col not in exclude_cols and df[col].dtype in ['int64', 'float64']]
    
    # Create binary classification target based on median yield
    median_yield = df['Crop_Yield_MT_per_HA'].median()
    df['Yield_Category'] = (df['Crop_Yield_MT_per_HA'] > median_yield).astype(int)
    
    X = df[feature_cols]
    y = df['Yield_Category']
    
    print(f"Features used ({len(feature_cols)}): {feature_cols[:5]}...")
    print(f"Target distribution:\n{y.value_counts()}")
    
    return X, y, feature_cols

def create_confusion_matrix_plot(y_true, y_pred, save_path='confusion_matrix.png'):
    """Create and save confusion matrix plot"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.title('Confusion Matrix - Crop Yield Prediction', fontsize=14, fontweight='bold')
    plt.ylabel('Actual', fontsize=12)
    plt.xlabel('Predicted', fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Confusion matrix saved to {save_path}")
    return save_path

def create_feature_importance_plot(model, feature_names, save_path='feature_importance.png', top_n=15):
    """Create and save feature importance plot"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    plt.figure(figsize=(10, 6))
    plt.title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
    plt.barh(range(top_n), importances[indices], color='steelblue')
    plt.yticks(range(top_n), [feature_names[i] for i in indices])
    plt.xlabel('Importance Score', fontsize=12)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Feature importance plot saved to {save_path}")
    return save_path

def create_roc_curve_plot(y_true, y_pred_proba, save_path='roc_curve.png'):
    """Create and save ROC curve plot"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = roc_auc_score(y_true, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ ROC curve saved to {save_path}")
    return save_path

def save_classification_report(y_true, y_pred, save_path='classification_report.txt'):
    """Save classification report to text file"""
    report = classification_report(y_true, y_pred)
    with open(save_path, 'w') as f:
        f.write("Classification Report - Crop Yield Prediction\n")
        f.write("=" * 60 + "\n")
        f.write(report)
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"✅ Classification report saved to {save_path}")
    return save_path

def train_model_with_tuning(use_dagshub=False):
    """Train model with hyperparameter tuning and manual logging"""
    
    # Setup MLflow tracking
    tracking_uri = setup_mlflow_tracking(use_dagshub)
    
    # Set experiment name
    mlflow.set_experiment("Climate_Change_Agriculture_Advanced")
    
    # Load data
    X, y, feature_names = load_and_prepare_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Training set size: {X_train.shape}")
    print(f"📊 Test set size: {X_test.shape}")
    
    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    print(f"\n🔧 Hyperparameter grid: {param_grid}")
    
    # Start MLflow run with manual logging
    with mlflow.start_run(run_name=f"RandomForest_Tuned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        
        # Log dataset info
        mlflow.log_param("dataset_name", "climate_change_preprocessing.csv")
        mlflow.log_param("dataset_shape", f"{X.shape[0]}x{X.shape[1]}")
        mlflow.log_param("train_size", X_train.shape[0])
        mlflow.log_param("test_size", X_test.shape[0])
        mlflow.log_param("test_split_ratio", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("num_features", len(feature_names))
        
        # Hyperparameter tuning with GridSearchCV
        print("\n🔍 Starting hyperparameter tuning with GridSearchCV...")
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42, n_jobs=-1),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        
        # Log best hyperparameters
        print("\n✅ Best hyperparameters found:")
        for param, value in grid_search.best_params_.items():
            print(f"  - {param}: {value}")
            mlflow.log_param(f"best_{param}", value)
        
        # Cross-validation scores
        cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='accuracy')
        
        # Train set predictions
        y_train_pred = best_model.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_train_pred)
        
        # Test set predictions
        y_test_pred = best_model.predict(X_test)
        y_test_pred_proba = best_model.predict_proba(X_test)[:, 1]
        
        # Calculate standard metrics (like autolog)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        precision = precision_score(y_test, y_test_pred, average='weighted')
        recall = recall_score(y_test, y_test_pred, average='weighted')
        f1 = f1_score(y_test, y_test_pred, average='weighted')
        
        # Calculate additional metrics (beyond autolog)
        roc_auc = roc_auc_score(y_test, y_test_pred_proba)
        overfitting_measure = train_accuracy - test_accuracy
        
        # Manual logging of standard metrics
        mlflow.log_metric("test_accuracy", test_accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Manual logging of additional metrics (ADVANCED requirement)
        mlflow.log_metric("roc_auc_score", roc_auc)
        mlflow.log_metric("train_accuracy", train_accuracy)
        mlflow.log_metric("cv_mean_score", cv_scores.mean())
        mlflow.log_metric("cv_std_score", cv_scores.std())
        mlflow.log_metric("best_cv_score", grid_search.best_score_)
        mlflow.log_metric("overfitting_measure", overfitting_measure)
        
        # Print metrics
        print("\n📈 Model Performance Metrics:")
        print(f"  Test Accuracy: {test_accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        print(f"  ROC AUC: {roc_auc:.4f} [ADDITIONAL]")
        print(f"  Train Accuracy: {train_accuracy:.4f} [ADDITIONAL]")
        print(f"  CV Mean Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f}) [ADDITIONAL]")
        print(f"  Best CV Score: {grid_search.best_score_:.4f} [ADDITIONAL]")
        print(f"  Overfitting Measure: {overfitting_measure:.4f} [ADDITIONAL]")
        
        # Create and log artifacts
        print("\n📊 Creating and logging artifacts...")
        
        # 1. Confusion Matrix
        cm_path = create_confusion_matrix_plot(y_test, y_test_pred)
        mlflow.log_artifact(cm_path)
        
        # 2. Feature Importance
        fi_path = create_feature_importance_plot(best_model, feature_names)
        mlflow.log_artifact(fi_path)
        
        # 3. ROC Curve (Additional artifact for ADVANCED)
        roc_path = create_roc_curve_plot(y_test, y_test_pred_proba)
        mlflow.log_artifact(roc_path)
        
        # 4. Classification Report (Additional artifact for ADVANCED)
        cr_path = save_classification_report(y_test, y_test_pred)
        mlflow.log_artifact(cr_path)
        
        # Log the model (FIXED VERSION - Compatible with MLflow 2.9.2)
        print("\n💾 Logging model to MLflow...")
        
        # Create model artifacts directory
        os.makedirs("model_artifacts", exist_ok=True)
        model_path = "model_artifacts/random_forest_model.pkl"
        
        # Save model as pickle file
        joblib.dump(best_model, model_path)
        print(f"  ✅ Model saved as: {model_path}")
        
        # Log model as artifact (always works)
        mlflow.log_artifact(model_path, artifact_path="model")
        print(f"  ✅ Model logged as artifact successfully!")
        
        # Try to log with mlflow.sklearn (with error handling for compatibility)
        try:
            mlflow.sklearn.log_model(
                sk_model=best_model,
                artifact_path="sklearn_model"
            )
            print(f"  ✅ Model logged with mlflow.sklearn successfully!")
        except Exception as e:
            print(f"  ⚠️ Note: mlflow.sklearn logging skipped (not supported by server)")
            print(f"     Model is still available as pickle artifact in 'model' folder")
        
        # Log additional tags
        mlflow.set_tag("model_type", "Random Forest Classifier")
        mlflow.set_tag("tuning_method", "GridSearchCV")
        mlflow.set_tag("author", "Zidan Mubarak")
        mlflow.set_tag("dataset", "Climate Change Agriculture")
        mlflow.set_tag("task", "Binary Classification")
        
        print("\n✅ Model and all artifacts logged successfully!")
        print(f"\n🌐 View results at: {tracking_uri}")

def main():
    """Main function with user interaction"""
    print("="*70)
    print("KRITERIA 2 - ADVANCED (4 pts)")
    print("Model Training with Hyperparameter Tuning & DagsHub Integration")
    print("="*70)
    
    # Ask user for DagsHub integration
    print("\n" + "="*70)
    print("TRACKING OPTIONS")
    print("="*70)
    print("Pilih tracking method:")
    print("1. Local MLflow only (Skilled - 3 pts)")
    print("2. DagsHub MLflow (Advanced - 4 pts)")
    
    choice = input("\nMasukkan pilihan (1/2) [default: 1]: ").strip()
    use_dagshub = (choice == "2")
    
    if use_dagshub and not DAGSHUB_AVAILABLE:
        print("\n❌ dagshub library not installed!")
        print("   Install with: pip install dagshub")
        print("   Falling back to local MLflow...")
        use_dagshub = False
    
    # Train model
    train_model_with_tuning(use_dagshub)
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETED!")
    print("="*70)
    print("\n📊 Features implemented:")
    print("  ✓ Hyperparameter tuning with GridSearchCV")
    print("  ✓ Manual logging (not autolog)")
    print("  ✓ Standard metrics: accuracy, precision, recall, f1")
    print("  ✓ Additional metrics (6): ROC AUC, train accuracy, CV scores, overfitting")
    print("  ✓ Artifacts (4): confusion matrix, feature importance, ROC curve, report")
    print("  ✓ Model saved as pickle + artifact")
    if use_dagshub:
        print("  ✓ DagsHub integration enabled")
    print("="*70)
    print("\n📝 Model deployment:")
    print("  import joblib")
    print("  model = joblib.load('model_artifacts/random_forest_model.pkl')")
    print("="*70)

if __name__ == "__main__":
    main()