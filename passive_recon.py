#!/usr/bin/env python3
"""
XZ Labs - Passive Recon Engine (Sentinel Core)
"""
import sys
import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SentinelPassive")

class PassiveEngine:
    def __init__(self, target_domain: str):
        self.target = target_domain.strip().lower()
        self.subdomains = set()

    def fetch_ct_logs(self) -> set:
        logger.info(f"Querying CT logs for: {self.target}")
        url = f"https://crt.sh/?q=%25.{self.target}&output=json"
        try:
            response = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                for entry in response.json():
                    names = entry.get("name_value", "").split("\n")
                    for name in names:
                        clean_name = name.strip().lower()
                        if clean_name.endswith(self.target) and not clean_name.startswith("*."):
                            self.subdomains.add(clean_name)
            logger.info(f"Extracted {len(self.subdomains)} unique domains.")
        except Exception as e:
            logger.error(f"Error reading CT logs: {str(e)}")
        return self.subdomains

    def compile_report(self):
        return json.dumps({"target": self.target, "discovered_hosts": sorted(list(self.subdomains))}, indent=4)

def main():
    if len(sys.argv) < 2:
        print("Usage: python passive_recon.py <domain>")
        sys.exit(1)
    target = sys.argv[1]
    engine = PassiveEngine(target)
    engine.fetch_ct_logs()
    print(engine.compile_report())

if __name__ == "__main__":
    main()
