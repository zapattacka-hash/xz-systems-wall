#!/usr/bin/env python3
"""
XZ Labs - Environment Target Filter
Parses raw subdomain listings to isolate non-production infrastructure.
"""
import sys
import json

# Target keyword signatures for non-production environments
ENV_SIGNATURES = ['stage', 'stg', 'dev', 'test', 'qa', 'perf', 'uat', 'internal', 'local']

def filter_subdomains(input_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        hosts = data.get("discovered_hosts", [])
        isolated_targets = []

        for host in hosts:
            # Check if any non-prod signature exists in the hostname segments
            if any(sig in host for sig in ENV_SIGNATURES):
                isolated_targets.append(host)

        report = {
            "target_root": data.get("target"),
            "total_raw_hosts": len(hosts),
            "isolated_env_hosts_count": len(isolated_targets),
            "isolated_hosts": sorted(isolated_targets)
        }
        
        print(json.dumps(report, indent=4))

    except FileNotFoundError:
        print(f"[-] Error: Input file '{input_file}' not found.")
    except json.JSONDecodeError:
        print("[-] Error: Invalid JSON format in input file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_env.py <results_json_file>")
        sys.exit(1)
    filter_subdomains(sys.argv[1])
