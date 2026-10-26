"""
Kriteria 4: Monitoring dan Logging - Inference Client
Dataset: Climate Change Impact on Agriculture 2024
Author: Zidan Mubarak
Description: Client untuk consume model dari Docker container (URL-based serving)

"""

import requests
import json
import time

# Docker container URL (dari Kriteria 3)
DOCKER_API_URL = "http://localhost:5002"

def check_model_health():
    """Check if Docker container model is healthy"""
    try:
        response = requests.get(f"{DOCKER_API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model Status: {data.get('status')}")
            print(f"✅ Model Loaded: {data.get('model_loaded')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Docker container at {DOCKER_API_URL}")
        print("   Make sure Docker container is running:")
        print("   docker run -d --name climate-ml-api -p 5002:5000 zidanmubarak/climate-change-ml:latest")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def make_prediction(features):
    """
    Make prediction using Docker container API (URL-based)
    
    Args:
        features: List of feature values
        
    Returns:
        dict: Prediction result from Docker API
    """
    try:
        payload = {"features": features}
        
        print(f"\n📤 Sending request to Docker API: {DOCKER_API_URL}/predict")
        print(f"   Features: {features[:5]}... (showing first 5)")
        
        start_time = time.time()
        response = requests.post(
            f"{DOCKER_API_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Prediction received from Docker API:")
            print(f"   Prediction: {result.get('prediction')}")
            print(f"   Label: {result.get('prediction_label')}")
            print(f"   Probability: {result.get('probability')}")
            print(f"   Response time: {duration:.3f}s")
            return result
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Docker container at {DOCKER_API_URL}")
        return None
    except Exception as e:
        print(f"❌ Error making prediction: {e}")
        return None

def test_inference():
    """Test inference using Docker container API"""
    print("="*70)
    print("CLIMATE CHANGE ML INFERENCE CLIENT")
    print("Using Docker Container API (URL-based serving)")
    print("="*70)
    
    # Check if Docker container is healthy
    print("\n1. Checking Docker container health...")
    if not check_model_health():
        print("\n❌ Docker container is not accessible!")
        print("\nPlease start the Docker container first:")
        print("  docker pull zidanmubarak/climate-change-ml:latest")
        print("  docker run -d --name climate-ml-api -p 5002:5000 zidanmubarak/climate-change-ml:latest")
        return
    
    # Example features for climate change model (18 features)
    print("\n2. Making prediction via Docker API...")
    sample_features = [
        2024,    # Year
        25.5,    # Average_Temperature_C
        1200,    # Total_Precipitation_mm
        500,     # CO2_Emissions_MT
        5,       # Crop_Yield_MT_per_HA
        3.5,     # Extreme_Weather_Events
        80,      # Irrigation_Access_Percent
        15,      # Pesticide_Use_KG_per_HA
        7.5,     # Fertilizer_Use_KG_per_HA
        2.5,     # Soil_Health_Index
        1,       # Adaptation_Strategies
        0,       # Economic_Impact_Million_USD
        1,       # Region_encoded
        0,       # Country_encoded
        0,       # Crop_Type_encoded
        1,       # Season_encoded
        0,       # Additional features
        0
    ]
    
    result = make_prediction(sample_features)
    
    if result:
        print("\n✅ Inference successful!")
        print("\nKEY POINT:")
        print("  - Model di-serve via Docker container URL")
        print(f"  - API URL: {DOCKER_API_URL}")
    else:
        print("\n❌ Inference failed!")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_inference()
