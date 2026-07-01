# 🦊 watch-my-kids

**Firefox Usage Monitor**

A lightweight, silent background tool to monitor and log open tabs in Mozilla Firefox on macOS.

## 🌟 Features

- **Silent Monitoring**: Reads Firefox's session backup files (`recovery.jsonlz4`) directly. No need for invasive browser extensions or accessibility permissions.
- **Smart Logging**: Logs changes every minute. If tabs haven't changed, it stays silent to save space.
- **Daily Archives**: Automatically organizes logs into daily files (e.g., `logs/2026-07-01.log`).
- **Stealth**: Hidden by default (dot-files), runs in the background via cron.

## 📂 Directory Structure

```text
watch-my-kids/
├── monitor.py        # Core monitoring script
├── setup.sh          # One-click installation script
├── logs/             # [Auto-generated] Daily log files (Ignored by git)
└── README.md         # Documentation
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd watch-my-kids
chmod +x setup.sh
./setup.sh
```

This script will:
1. Install the required `lz4` python library.
2. Set up a `crontab` to run the monitor every minute.

### 2. Viewing Logs

Logs are saved in the `logs/` directory.

```bash
# View today's log
cat logs/$(date +%Y-%m-%d).log

# View recent history
tail -f logs/$(date +%Y-%m-%d).log

# Search for specific keywords
grep -i "youtube" logs/*.log
```

## 🛠️ Manual Usage

If you don't want the background service, you can run it manually to test:

```bash
pip3 install lz4
python3 monitor.py
```

## 📝 Log Format

Each log entry looks like this:

```text
--- Snapshot at 10:30:15 ---
[Bilibili - Homepage] https://www.bilibili.com/
[GitHub] https://github.com/
```

## ⚠️ Note

- **Compatibility**: Designed for macOS and Firefox.
- **Privacy**: Logs are stored locally. Please use responsibly.
