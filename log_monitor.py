#!/usr/bin/env python3
import csv
from datetime import datetime

def parse_time(time_str):
    """Convert HH:MM:SS to datetime object"""
    return datetime.strptime(time_str, '%H:%M:%S')

def process_logs(filename):
    """Process log file and calculate job durations"""
    jobs = {}  # PID -> [job_name, start_time]
    completed_jobs = []
    
    # Read and parse CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            time_str, job_name, action, pid = row
            timestamp = parse_time(time_str.strip())
            pid = int(pid.strip())
            action = action.strip()
            
            if action == 'START':
                jobs[pid] = [job_name.strip(), timestamp]
            elif action == 'END':
                if pid in jobs:
                    job_name, start_time = jobs[pid]
                    duration_seconds = (timestamp - start_time).total_seconds()
                    duration_minutes = duration_seconds / 60
                    
                    completed_jobs.append({
                        'name': job_name,
                        'pid': pid,
                        'duration_minutes': duration_minutes,
                        'duration_seconds': duration_seconds
                    })
                    del jobs[pid]
    
    return completed_jobs

def generate_report(jobs):
    """Generate warning/error report"""
    print("=" * 50)
    print("LOG MONITORING REPORT")
    print("=" * 50)
    
    errors = 0
    warnings = 0
    
    # Sort by duration (longest first)
    jobs.sort(key=lambda x: x['duration_minutes'], reverse=True)
    
    for job in jobs:
        name = job['name']
        pid = job['pid']
        minutes = job['duration_minutes']
        
        if minutes > 10:  # Error threshold
            print(f"ERROR: {name} (PID: {pid}) took {minutes:.2f} minutes")
            errors += 1
        elif minutes > 5:  # Warning threshold
            print(f"WARNING: {name} (PID: {pid}) took {minutes:.2f} minutes")
            warnings += 1
        else:
            print(f"PASSED: {name} (PID: {pid}) took {minutes:.2f} minutes")
    
    print("=" * 50)
    print(f"Total jobs: {len(jobs)}")
    print(f"Errors (>10 min): {errors}")
    print(f"Warnings (5-10 min): {warnings}")
    print(f"Normal (<5 min): {len(jobs) - errors - warnings}")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python log_monitor.py <log_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        jobs = process_logs(filename)
        generate_report(jobs)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
