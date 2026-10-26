# Kriteria 4: Monitoring dan Logging

**Dataset**: Climate Change Impact on Agriculture 2024  
**Author**: Zidan Mubarak  

## Overview

Mengimplementasikan monitoring dan logging untuk model machine learning Climate Change Agriculture dengan:
- **Model serving**: Pull Docker image dari Docker Hub (hasil Kriteria 3)
- **Monitoring**: Prometheus dengan 13+ metrics
- **Visualisasi**: Grafana dashboard
- **Alerting**: 3 rules untuk anomaly detection

---

## Struktur Folder

```
Monitoring_dan_Logging/
├── 1.bukti_serving/                      # Screenshots Docker serving
├── 2.prometheus.yml                      # Prometheus configuration
├── 3.prometheus_exporter.py              # Custom Prometheus exporter
├── 4.bukti_monitoring_Prometheus/        # Screenshots Prometheus (10+ metrics)
├── 5.bukti_monitoring_Grafana/           # Screenshots Grafana (10+ metrics)
├── 6.bukti_alerting_Grafana/             # Screenshots alerting (3 rules)
├── 7.inference.py                        # Client untuk consume Docker API
├── requirements.txt                      # Dependencies
└── README.md                             # Dokumentasi ini
```

---

## Cara Menjalankan

### Step 1: Pull dan Run Docker Image (Model Serving)

```bash
# Pull image dari Docker Hub (hasil Kriteria 3)
docker pull zidanmubarak/climate-change-ml:latest

# Run container dengan Flask API
docker run -d \
  --name climate-ml-api \
  -p 5002:5000 \
  zidanmubarak/climate-change-ml:latest

# Verify container is running
docker ps

# Check logs
docker logs climate-ml-api
```

**Expected output dari logs:**
```
✅ Model loaded from model/random_forest_model.pkl
 * Serving Flask app 'serve_model'
 * Running on http://0.0.0.0:5000
```

### Step 2: Verify Model Serving (URL-based)

```bash
# Test health endpoint
curl http://localhost:5002/health

# Expected response:
# {"status": "healthy", "model_loaded": true}

# Test prediction endpoint
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\": [2024, 25.5, 1200, 500, 5, 3.5, 80, 15, 7.5, 2.5, 1, 0, 1, 0, 0, 1, 0, 0]}"

# Expected response:
# {"prediction": 1, "prediction_label": "High Yield", ...}
```

### Step 3: Start Prometheus Exporter

**Terminal 1:**
```bash
cd d:\kuliah\sem7\asah\submission\tes\Monitoring_dan_Logging
python 3.prometheus_exporter.py
```

Output: `Starting Prometheus exporter on port 8001`

### Step 4: Start Prometheus

**Terminal 2:**
```bash
cd d:\kuliah\sem7\asah\submission\tes\Monitoring_dan_Logging
prometheus --config.file=2.prometheus.yml
```

Access: http://localhost:9090

### Step 5: Start Grafana

```bash
# Windows: Start Grafana service
# Linux: sudo systemctl start grafana-server
```

Access: http://localhost:3000 (admin/admin)

---

## Docker Container Details

### Image Information

- **Image**: `zidanmubarak/climate-change-ml:latest`
- **Built by**: GitHub Actions CI/CD (Kriteria 3)
- **Contains**: Flask API + Trained Model
- **Endpoints**:
  - `GET /` - Home
  - `GET /health` - Health check
  - `POST /predict` - Prediction

### Port Mapping

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Flask API (Docker) | 5000 | 5002 | http://localhost:5002 |
| Prometheus Exporter | - | 8001 | http://localhost:8001 |
| Prometheus | 9090 | 9090 | http://localhost:9090 |
| Grafana | 3000 | 3000 | http://localhost:3000 |

---

## Monitoring Architecture

```
┌─────────────────────────────────────────┐
│  Docker Container (Kriteria 3)          │
│  zidanmubarak/climate-change-ml:latest │
│  Flask API serving model via URL        │
│  Port: 5002                             │
│  Endpoints: /health, /predict           │
└─────────────────┬───────────────────────┘
                  │
                  ↓ monitored by
┌─────────────────────────────────────────┐
│  Prometheus Exporter                    │
│  (3.prometheus_exporter.py)             │
│  Port: 8001                             │
│  Checks: http://localhost:5002/health   │
│  Metrics: 13 system & API metrics       │
└─────────────────┬───────────────────────┘
                  │
                  ↓ scraped by
┌─────────────────────────────────────────┐
│  Prometheus                             │
│  Port: 9090                             │
│  Stores metrics & evaluates alerts      │
└─────────────────┬───────────────────────┘
                  │
                  ↓ visualized by
┌─────────────────────────────────────────┐
│  Grafana                                │
│  Port: 3000                             │
│  Dashboard + Alerting                   │
└─────────────────────────────────────────┘
```

---

## Metrics Available (13 Metrics)

**From Custom Exporter** (monitoring Docker container):

1. `custom_cpu_usage_percent` - CPU usage
2. `custom_memory_usage_percent` - Memory usage
3. `custom_disk_usage_percent` - Disk usage
4. `custom_network_bytes_sent_total` - Network sent
5. `custom_network_bytes_recv_total` - Network received
6. `custom_process_count` - Process count
7. `custom_thread_count` - Thread count
8. `custom_api_health_status` - **Docker API health** (checks URL)
9. `custom_api_response_time_seconds` - **API response time** (from URL)
10. `custom_model_availability` - **Model availability** (from URL)
11. `custom_system_load_1min` - 1-min load
12. `custom_system_load_5min` - 5-min load
13. `custom_system_load_15min` - 15-min load

**Total**: 13+ metrics (melebihi requirement 10 untuk Advanced!)