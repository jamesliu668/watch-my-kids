#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
watch-my-kids: Firefox Usage Monitor
Monitors active tabs in Firefox by parsing recovery.jsonlz4
"""

import os
import sys
import json
import glob
import datetime
import hashlib
import lz4.block

# --- Configuration ---
# Base path for Firefox profiles (macOS default)
FIREFOX_PROFILES_DIR = os.path.expanduser("~/Library/Application Support/Firefox/Profiles")

# Directories for the project
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")
STATE_FILE = os.path.join(PROJECT_DIR, ".monitor_state")

def find_recovery_file():
    """Find the most recent recovery.jsonlz4 file in any default profile."""
    pattern = os.path.join(FIREFOX_PROFILES_DIR, "*.default-release", "sessionstore-backups", "recovery.jsonlz4")
    files = glob.glob(pattern)
    
    # Fallback for older profiles
    if not files:
        pattern = os.path.join(FIREFOX_PROFILES_DIR, "*.default", "sessionstore-backups", "recovery.jsonlz4")
        files = glob.glob(pattern)

    if not files:
        return None
    
    # Return the one with the most recent modification time
    return max(files, key=os.path.getmtime)

def get_active_tabs(filepath):
    """Parse the jsonlz4 file and return a list of (url, title) tuples."""
    try:
        with open(filepath, 'rb') as f:
            f.read(8)  # Skip magic header "mozLz40\0"
            compressed_data = f.read()
            json_data = lz4.block.decompress(compressed_data)
            session = json.loads(json_data)
        
        tabs = []
        for window in session.get('windows', []):
            for tab in window.get('tabs', []):
                entries = tab.get('entries', [])
                index = tab.get('index', 1) - 1
                if 0 <= index < len(entries):
                    entry = entries[index]
                    url = entry.get('url', '')
                    title = entry.get('title', 'No Title')
                    if url and url.startswith('http'):
                        tabs.append((url, title))
        return tabs
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return []

def get_state():
    """Load the previous state hash."""
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, 'r') as f:
        return f.read().strip()

def save_state(content_hash):
    """Save the current state hash."""
    with open(STATE_FILE, 'w') as f:
        f.write(content_hash)

def log_tabs(tabs):
    """Append current tabs to a daily log file."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOGS_DIR, f"{date_str}.log")
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Snapshot at {timestamp} ---\n")
        for url, title in tabs:
            f.write(f"[{title}] {url}\n")

def main():
    recovery_file = find_recovery_file()
    if not recovery_file:
        print("Firefox recovery file not found. Is Firefox running?", file=sys.stderr)
        sys.exit(1)

    # 1. Get current tabs
    current_tabs = get_active_tabs(recovery_file)
    if not current_tabs:
        # Could be a private window or just loading
        return 

    # 2. Check for changes
    # Create a sorted string representation to detect changes regardless of order
    content_repr = "\n".join(sorted([f"{u}|{t}" for u, t in current_tabs]))
    current_hash = hashlib.md5(content_repr.encode('utf-8')).hexdigest()
    
    last_hash = get_state()
    
    if current_hash != last_hash:
        # State changed, log it!
        log_tabs(current_tabs)
        save_state(current_hash)
        # print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] State updated and logged.")
    else:
        # No change, silence is golden
        pass

if __name__ == "__main__":
    main()
