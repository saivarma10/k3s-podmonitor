#!/bin/bash
# Replace these with your actual values
NAMESPACE="default"

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <POD_NAME_1> [<POD_NAME_2> ...]"
    exit 1
fi

POD_NAMES=("$@")

while true; do
    # Get current timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Iterate over each pod name
    for POD_NAME in "${POD_NAMES[@]}"; do
        # Get CPU and memory usage metrics using kubectl top
        METRICS=$(kubectl top pod "$POD_NAME" -n "$NAMESPACE" --containers)
        
        # Extract total CPU and memory usage for the pod
        MEMORY_USAGE=$(echo "$METRICS" | awk 'NR>1{sum+=$4} END{print sum}')
        CPU_USAGE=$(echo "$METRICS" | awk 'NR>1{sum+=$3} END{print sum}')
        
        # Generate JSON object with metrics for the specific pod
        JSON="{ \"timestamp\": \"$TIMESTAMP\", \"cpu\": \"$CPU_USAGE\", \"memory\": \"$MEMORY_USAGE\" }"
        
        # Define the output file name based on the pod name
        OUTPUT_FILE="${POD_NAME}_metrics.json"
        
        # Write JSON to the output file
        echo "$JSON" >> "$OUTPUT_FILE"
    done
    
    # Sleep for 5 seconds
    sleep 5
done
