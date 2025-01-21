# k3s-podmonitor

## Overview
`k3s-podmonitor` is a monitoring solution designed to track CPU and memory usage of specified Kubernetes pods. It includes a Bash script for collecting pod metrics using `kubectl` and a Flask-based web server for processing and exporting the data to Excel files.

## Features
- Real-time monitoring of CPU and memory usage for specified Kubernetes pods.
- Storage of pod metrics in JSON format.
- Web interface to view and download metrics.
- Export collected metrics to Excel for further analysis.

## Project Structure
```
newfinal/
├── metrics_test2.py      # Flask web application
├── new.sh                # Bash script for collecting metrics
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates for Flask app
```

## Prerequisites
- Kubernetes cluster with `kubectl` configured.
- Python 3.10+ installed.
- Required Python packages (see `requirements.txt`).

## Installation

### 1. Install Dependencies
Ensure Python dependencies are installed:
```bash
pip3 install -r requirements.txt
```

### 2. Run the Monitoring Script
To start monitoring pods, execute the script with pod names as arguments:
```bash
bash new.sh pod1 pod2 pod3
```
The script will collect CPU and memory usage data every 5 seconds and store them in JSON files named `<pod_name>_metrics.json`.

### 3. Run the Flask Application
Start the Flask web server to access collected metrics:
```bash
python3 metrics_test2.py --ip 0.0.0.0 --port 5486
```

## Usage

### Monitoring Kubernetes Pods
Run the monitoring script with the desired pod names to continuously log metrics:
```bash
bash new.sh my-pod-1 my-pod-2
```

### Accessing Metrics
Open your browser and visit:
```
http://<server-ip>:5486/stats/newfinal
```

### Exporting Metrics to Excel
To download an Excel file with aggregated metrics:
```
http://<server-ip>:5486/export/newfinal
```

## Bash Script Explanation (`new.sh`)
The script collects pod metrics and stores them in JSON format:
1. Takes pod names as arguments.
2. Uses `kubectl top` to fetch resource usage.
3. Extracts CPU and memory usage and writes to JSON files.
4. Runs indefinitely, collecting metrics every 5 seconds.

## Flask Application Explanation (`metrics_test2.py`)
The Flask app provides the following endpoints:

- `GET /export/<folder_name>`: Exports collected metrics as an Excel file.
- `GET /stats/<folder_name>`: Displays the metrics summary.

## Troubleshooting
- Ensure `kubectl` is configured correctly and has access to the cluster.
- Verify that pods exist and are running in the specified namespace.
- Check Flask logs for potential errors:
  ```bash
  tail -f flask.log
  ```

## Contributing
Feel free to submit issues and pull requests to improve the project.
