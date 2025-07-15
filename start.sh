#!/bin/bash
# Startup script that runs migrations before starting the bot

echo "Running database migrations..."
python migrate_db.py

echo "Starting the bot..."
python bot.py