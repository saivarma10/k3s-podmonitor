from flask import Flask, render_template, send_file
import argparse
import json
from datetime import datetime
import glob
import os
import pandas as pd
from openpyxl import load_workbook  # Import load_workbook from openpyxl
import xlwt
from xlwt import Workbook
from io import BytesIO

app = Flask(__name__)

def process_json_file(filename):
    metrics_data = []

    with open(filename, "r") as f:
        data = f.readlines()

    cpu_values = []
    memory_values = []

    for line in data:
        metric = json.loads(line)
        timestamp = datetime.strptime(metric["timestamp"], "%Y-%m-%d %H:%M:%S")

        # Add error handling for empty CPU and memory values
        try:
            cpu_value = int(metric["cpu"])
            memory_value = int(metric["memory"])
        except ValueError:
            # Handle the case where CPU or memory values are not valid integers
            # You can choose to skip this data point or handle it differently
            continue
        
        metrics_data.append({"timestamp": timestamp, "cpu": cpu_value, "memory": memory_value})
        
        cpu_values.append(cpu_value)
        memory_values.append(memory_value)

    if cpu_values:
        min_cpu = min(cpu_values)
        max_cpu = max(cpu_values)
        avg_cpu = sum(cpu_values) / len(cpu_values)
    else:
        min_cpu = max_cpu = avg_cpu = 0  # Handle the case of no valid CPU values

    if memory_values:
        min_memory = min(memory_values)
        max_memory = max(memory_values)
        avg_memory = sum(memory_values) / len(memory_values)
    else:
        min_memory = max_memory = avg_memory = 0  # Handle the case of no valid memory values

    return metrics_data, min_cpu, max_cpu, avg_cpu, min_memory, max_memory, avg_memory


@app.route('/export/<path:folder_name>', methods=['GET'])
def export_to_excel(folder_name):
    matching_files = glob.glob(os.path.join(folder_name, '*.json'))

    file_stats_list = []

    for file in matching_files:
        _, min_cpu, max_cpu, avg_cpu, min_memory, max_memory, avg_memory = process_json_file(file)
        
        file_stats = {
            "file": os.path.basename(file),
            "min_cpu": min_cpu,
            "max_cpu": max_cpu,
            "avg_cpu": avg_cpu,
            "min_memory": min_memory,
            "max_memory": max_memory,
            "avg_memory": avg_memory
        }
        file_stats_list.append(file_stats)

    # Create a DataFrame from the file_stats_list
    df = pd.DataFrame(file_stats_list)

    # Create an Excel writer object with the XlsxWriter engine
    excel_writer = pd.ExcelWriter('metrics_data.xlsx', engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    df.to_excel(excel_writer, sheet_name='Metrics Data', index=False)

    # Close the Excel writer (this will also save the file)
    excel_writer.close()

    # Return the Excel file as a response
    return send_file('metrics_data.xlsx', as_attachment=True, download_name='metrics_data.xlsx')

@app.route('/stats/<path:folder_name>', methods=['GET'])
def get_metrics(folder_name):
    metrics_data = []

    matching_files = glob.glob(os.path.join(folder_name, '*.json'))

    file_stats_list = []

    for file in matching_files:
        file_metrics, min_cpu, max_cpu, avg_cpu, min_memory, max_memory, avg_memory = process_json_file(file)
        metrics_data.extend(file_metrics)
        
        file_stats = {
            "file": os.path.basename(file),
            "min_cpu": min_cpu,
            "max_cpu": max_cpu,
            "avg_cpu": avg_cpu,
            "min_memory": min_memory,
            "max_memory": max_memory,
            "avg_memory": avg_memory,
            "metrics": file_metrics  # Include metrics data for each file
        }
        file_stats_list.append(file_stats)

    return render_template('stats2.html', file_stats_list=file_stats_list)

@app.route('/favicon.ico')
def favicon():
    return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run metrics server.')
    parser.add_argument('--ip', type=str, default='localhost', help='IP address to run the server on')
    parser.add_argument('--port', type=int, default=5486, help='Port to run the server on')
    args = parser.parse_args()
    app.run(host=args.ip, port=args.port)
