"""
Kriteria 4: Monitoring dan Logging - Prometheus Exporter
Dataset: Climate Change Impact on Agriculture 2024
Author: Zidan Mubarak
Description: Custom Prometheus exporter untuk monitoring tambahan
"""

from prometheus_client import start_http_server, Gauge, Counter, Histogram
import psutil
import time
import requests
from datetime import datetime

# Custom metrics untuk monitoring sistem
# 1. System metrics
cpu_usage_percent = Gauge('custom_cpu_usage_percent', 'CPU usage percentage')
memory_usage_percent = Gauge('custom_memory_usage_percent', 'Memory usage percentage')
disk_usage_percent = Gauge('custom_disk_usage_percent', 'Disk usage percentage')

# 2. Network metrics
network_bytes_sent = Counter('custom_network_bytes_sent_total', 'Total bytes sent over network')
network_bytes_recv = Counter('custom_network_bytes_recv_total', 'Total bytes received over network')

# 3. Process metrics
process_count = Gauge('custom_process_count', 'Number of running processes')
thread_count = Gauge('custom_thread_count', 'Number of threads')

# 4. API health metrics
api_health_status = Gauge('custom_api_health_status', 'API health status (1=healthy, 0=unhealthy)')
api_response_time = Histogram('custom_api_response_time_seconds', 'API response time in seconds')

# 5. Model metrics
model_availability = Gauge('custom_model_availability', 'Model availability (1=available, 0=unavailable)')

# 6. System load
system_load_1min = Gauge('custom_system_load_1min', '1-minute system load average')
system_load_5min = Gauge('custom_system_load_5min', '5-minute system load average')
system_load_15min = Gauge('custom_system_load_15min', '15-minute system load average')

def collect_system_metrics():
    """Collect system metrics"""
    try:
        # CPU usage
        cpu_usage_percent.set(psutil.cpu_percent(interval=1))
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage_percent.set(memory.percent)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage_percent.set(disk.percent)
        
        # Network stats
        net_io = psutil.net_io_counters()
        network_bytes_sent.inc(net_io.bytes_sent)
        network_bytes_recv.inc(net_io.bytes_recv)
        
        # Process count
        process_count.set(len(psutil.pids()))
        
        # Thread count
        total_threads = sum([p.num_threads() for p in psutil.process_iter(['num_threads'])])
        thread_count.set(total_threads)
        
        # System load (Unix-like systems)
        try:
            load_avg = psutil.getloadavg()
            system_load_1min.set(load_avg[0])
            system_load_5min.set(load_avg[1])
            system_load_15min.set(load_avg[2])
        except AttributeError:
            # Windows doesn't have getloadavg
            pass
        
    except Exception as e:
        print(f"Error collecting system metrics: {e}")

def check_api_health(api_url='http://localhost:5002/health'):
    """Check API health"""
    try:
        start_time = time.time()
        response = requests.get(api_url, timeout=5)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            api_health_status.set(1)
            try:
                model_availability.set(1 if response.json().get('model_loaded') else 0)
            except:
                model_availability.set(1)  # Assume loaded if can't parse JSON
        else:
            api_health_status.set(0)
            model_availability.set(0)
        
        api_response_time.observe(response_time)
        
    except requests.exceptions.ConnectionError:
        print(f"API not accessible at {api_url} - Make sure 7.inference.py is running")
        api_health_status.set(0)
        model_availability.set(0)
    except Exception as e:
        print(f"Error checking API health: {e}")
        api_health_status.set(0)
        model_availability.set(0)

def main():
    """Main function to run the exporter"""
    print("="*70)
    print("PROMETHEUS CUSTOM EXPORTER")
    print("="*70)
    print("Starting Prometheus exporter on port 8001")
    print("Metrics available at http://localhost:8001/metrics")
    print("="*70)
    
    # Start Prometheus HTTP server
    start_http_server(8001)
    
    # Collect metrics in loop
    while True:
        try:
            collect_system_metrics()
            check_api_health()
            time.sleep(5)  # Collect every 5 seconds
        except KeyboardInterrupt:
            print("\nShutting down exporter...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
