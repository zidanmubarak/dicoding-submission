"""
Kriteria 2: Membangun Model Machine Learning
Dataset: Climate Change Impact on Agriculture 2024
Author: Zidan Mubarak
Description: Model training dengan MLflow autolog (Basic level)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import mlflow.sklearn

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Set experiment name
mlflow.set_experiment("Climate_Change_Agriculture_Basic")

def load_and_prepare_data():
    """Load and prepare the preprocessed dataset"""
    print("📂 Loading preprocessed dataset...")
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
    
    print(f"Features: {len(feature_cols)} columns")
    print(f"Target distribution:\n{y.value_counts()}")
    
    return X, y

def train_model():
    """Train model with MLflow autolog"""
    
    # Load data
    X, y = load_and_prepare_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Enable MLflow autolog (BASIC requirement)
    mlflow.sklearn.autolog()
    
    # Start MLflow run
    with mlflow.start_run(run_name="RandomForest_Basic_Autolog"):
        
        print("\n🔧 Training Random Forest model...")
        
        # Train model with fixed hyperparameters
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✅ Model trained successfully!")
        print(f"📊 Test Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print("\n✅ Model and metrics logged automatically via autolog")
        print("🌐 View results at: http://127.0.0.1:5000")

if __name__ == "__main__":
    print("="*60)
    print("KRITERIA 2 - BASIC (2 pts)")
    print("Model Training with MLflow Autolog")
    print("="*60)
    
    train_model()
    
    print("\n" + "="*60)
    print("✅ Training completed!")
    print("📊 Check MLflow UI at: http://127.0.0.1:5000")
    print("="*60)
