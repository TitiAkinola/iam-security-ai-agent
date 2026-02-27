import os

# SRE Tool: Log Parser for Incident Diagnostics
# Goal: Reduce MTTR by filtering critical errors from system logs.

def parse_logs(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    # Initialize counters for SRE reporting
    total_lines = 0
    alerts_found = 0
    malformed_lines = 0

    print(f"--- Scanning {file_path} for Critical Issues ---")
    
    with open(file_path, 'r') as file:
        for line in file:
            total_lines += 1
            try:
                # Logic: Only pull lines that require SRE attention
                # We strip the line early to avoid issues with trailing whitespace
                clean_line = line.strip()
                
                if "ERROR" in clean_line or "CRITICAL" in clean_line:
                    print(f"ALERT FOUND: {clean_line}")
                    alerts_found += 1
            
            except Exception as e:
                # If a line is corrupted or unreadable, we increment the skip counter
                malformed_lines += 1
                continue

    # Final Diagnostic Summary
    print("\n--- Diagnostic Summary ---")
    print(f"Total Lines Processed: {total_lines}")
    print(f"Critical Alerts Found: {alerts_found}")
    print(f"Malformed Lines Skipped: {malformed_lines}")

if __name__ == "__main__":
    # In a real SRE scenario, this would be a path to a GCP service log
    parse_logs("system.log")
