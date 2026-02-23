import pandas as pd
import sys
import os

# Thresholds
MAX_P99 = 800  # ms
MAX_ERROR_RATE = 0.1  # percent

def check_results(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Results file {file_path} not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
        
        # Locust stats file usually has a row for "Aggregated" or "Total"
        # We look for the last row or specific name
        total_row = df[df["Name"] == "Aggregated"]
        
        if total_row.empty:
            # Fallback to last row if Aggregated not found (older locust versions)
            total_row = df.iloc[-1:]
        
        p99 = total_row["99%"].values[0]
        failure_count = total_row["Failure Count"].values[0]
        request_count = total_row["Request Count"].values[0]
        
        error_rate = (failure_count / request_count) * 100 if request_count > 0 else 0
        
        print(f"Performance Metrics:")
        print(f"  P99 Response Time: {p99} ms (Threshold: {MAX_P99} ms)")
        print(f"  Error Rate: {error_rate:.2f}% (Threshold: {MAX_ERROR_RATE}%)")
        
        failed = False
        if p99 > MAX_P99:
            print("❌ P99 latency exceeded threshold.")
            failed = True
            
        if error_rate > MAX_ERROR_RATE:
            print("❌ Error rate exceeded threshold.")
            failed = True
            
        if failed:
            sys.exit(1)
            
        print("✅ Performance verification passed.")
        sys.exit(0)

    except Exception as e:
        print(f"Error analyzing results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_results.py <path_to_stats.csv>")
        sys.exit(1)
        
    check_results(sys.argv[1])
