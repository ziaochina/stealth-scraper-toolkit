"""
Production CLI & Docker Entrypoint for Stealth Scraper Toolkit
"""
import os
import sys
import logging
from stealth_scraper.engine import StealthScraperEngine

def main():
    target = os.getenv("TARGET_URL", "https://httpbin.org/headers")
    impersonate = os.getenv("BROWSER_PROFILE", "chrome124")
    
    print(f"[*] Starting Stealth Scraper Engine (Profile: {impersonate})...")
    engine = StealthScraperEngine(browser_profile=impersonate)
    
    print(f"[*] Dispatching protected request to: {target}")
    result = engine.fetch(target)
    
    if result:
        os.makedirs("./data", exist_ok=True)
        out_path = "./data/output.csv"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("target_url,status,payload_bytes,profile\n")
            f.write(f"{target},SUCCESS,{len(result)},{impersonate}\n")
        print(f"[+] Extraction complete. Results saved to {out_path}")
        print(f"[+] Engine Telemetry: {engine.metrics}")
    else:
        print("[-] Target request failed after max retries.")
        sys.exit(1)

if __name__ == "__main__":
    main()
