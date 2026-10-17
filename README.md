# Stealth Scraper & Anti-Bot Resilience Toolkit

Production-grade Python template for bypassing modern anti-bot protections (Cloudflare 5-second challenge, Turnstile, TLS JA4/HTTP2 fingerprinting, and 403 Forbidden rate limits) with Docker and proxy rotation.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Key Features

1. **TLS JA4/JA3 Fingerprint Spoofing**: Simulates authentic browser TLS handshakes (ciphers, extensions, curves) to defeat Layer-7 WAF fingerprinting;
2. **Turnstile / 5-Second Challenge Handling**: Built-in integration with C++ patched headless Chromium (`patchright`) and Camoufox engines;
3. **Exponential Backoff with Jitter**: Automatically recovers from transient `429 Too Many Requests` and network drops;
4. **Zero Host Pollution**: Fully containerized execution with non-root security compliance (`appuser`).

---

## 🚀 Quick Start (1-Command Run)

### Using Docker Compose (Recommended)
```bash
# 1. Clone repository
git clone https://github.com/ziaochina/stealth-scraper-toolkit.git
cd stealth-scraper-toolkit

# 2. Launch pipeline
docker compose up --build
```
Extracted data is automatically validated and saved to `./data/output.csv`.

### Using Local Python Virtualenv
```bash
pip install -r requirements.txt
python scraper.py
```

---

## ⚙️ Configuration & Environment Variables

| Variable | Description | Default | Mandatory |
| :--- | :--- | :--- | :---: |
| `TARGET_URL` | Target endpoint or search catalog | `https://example.com/catalog` | Yes |
| `MAX_CONCURRENCY` | Concurrent worker threads | `4` | No |
| `PROXY_URL` | Residential proxy gateway (http://user:pass@host:port) | `None` | No |
| `LOG_LEVEL` | Logging verbosity (DEBUG/INFO/WARN) | `INFO` | No |

---

## 📄 License
MIT License. Created by [Liujian Zhang](https://github.com/ziaochina).
