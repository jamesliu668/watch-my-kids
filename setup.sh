#!/bin/bash
# setup.sh - Install dependencies and configure cron for watch-my-kids

echo "🚀 Setting up watch-my-kids monitor..."

# 1. Install Python dependencies
echo "📦 Installing dependencies..."
pip3 install lz4

# 2. Create logs directory
mkdir -p "$(dirname "$0")/logs"

# 3. Setup Cron Job
CRON_JOB="* * * * * cd $(dirname "$0") && /usr/bin/python3 monitor.py"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "watch-my-kids"; then
    echo "✅ Cron job already exists, skipping."
else
    echo "⏱️  Adding cron job..."
    (crontab -l 2>/dev/null; echo "# watch-my-kids: Firefox Monitor"; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added (Runs every minute)."
fi

echo "🎉 Setup complete! Check logs in the 'logs' folder."
