import argparse
import collections
import json

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze server log files to find the top IP addresses.")
    
    parser.add_argument(
        'logfile',
        type=str,
        help='Path to the server log file'
    )
    
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Number of top IP addresses to display (default is 10)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output the result in JSON format'
    )
    
    return parser.parse_args()

def analyze_log(file_path, top_n):
    ip_counter = collections.Counter()
    
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                ip_address = line.split()[0]
                ip_counter[ip_address] += 1
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    return ip_counter.most_common(top_n)

def display_results(results, output_json):
    if output_json:
        print(json.dumps(dict(results), indent=4))
    else:
        for ip, count in results:
            print(f"{ip}: {count} requests")

def main():
    args = parse_args()
    results = analyze_log(args.logfile, args.top)
    display_results(results, args.json)

if __name__ == "__main__":
    main()