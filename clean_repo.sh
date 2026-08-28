#!/usr/bin/env bash

# Script to purge cache directories and compiled python files

echo "Purging __pycache__ and .pytest_cache directories..."
find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +

echo "Purging compiled .pyc files..."
find . -type f -name "*.pyc" -delete

echo "Cleanup complete!"