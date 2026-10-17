"""
Production Stealth Scraper Engine
Bypasses TLS JA4 fingerprints and rate-limiting using impersonated browser signatures.
"""
import os
import time
import logging
from typing import Optional
from curl_cffi import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class StealthScraper:
    def __init__(self, impersonate: str = "chrome124"):
        self.session = requests.Session(impersonate=impersonate)
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

    def fetch(self, url: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(1, max_retries + 1):
            try:
                logging.info(f"Connecting to {url} (Attempt {attempt}/{max_retries})...")
                resp = self.session.get(url, headers=self.headers, timeout=15)
                if resp.status_code == 200:
                    logging.info(f"Success: retrieved {len(resp.text)} bytes.")
                    return resp.text
                elif resp.status_code in (403, 429):
                    wait = 2 ** attempt
                    logging.warning(f"Status {resp.status_code} detected. Exponential backoff {wait}s...")
                    time.sleep(wait)
                else:
                    logging.warning(f"Unexpected status: {resp.status_code}")
            except Exception as e:
                logging.error(f"Network error on attempt {attempt}: {e}")
                time.sleep(2)
        return None

if __name__ == "__main__":
    target = os.getenv("TARGET_URL", "https://httpbin.org/headers")
    scraper = StealthScraper()
    output = scraper.fetch(target)
    if output:
        os.makedirs("./data", exist_ok=True)
        with open("./data/output.csv", "w", encoding="utf-8") as f:
            f.write("status,target,bytes_extracted\nSUCCESS," + target + "," + str(len(output)) + "\n")
        logging.info("Pipeline executed cleanly. Results written to ./data/output.csv")
