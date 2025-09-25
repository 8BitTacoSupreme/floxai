#!/usr/bin/env python3
"""
Simple backend test to check if dependencies are available
"""

import sys
import os

print("🐍 Python Test")
print("=" * 20)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

print("\n📦 Checking Dependencies")
print("=" * 25)

# Check if we can import required packages
try:
    import fastapi
    print("✅ FastAPI available")
except ImportError as e:
    print(f"❌ FastAPI not available: {e}")

try:
    import uvicorn
    print("✅ Uvicorn available")
except ImportError as e:
    print(f"❌ Uvicorn not available: {e}")

try:
    import sqlite3
    print("✅ SQLite3 available")
except ImportError as e:
    print(f"❌ SQLite3 not available: {e}")

try:
    import requests
    print("✅ Requests available")
except ImportError as e:
    print(f"❌ Requests not available: {e}")

try:
    import bs4
    print("✅ BeautifulSoup4 available")
except ImportError as e:
    print(f"❌ BeautifulSoup4 not available: {e}")

print("\n🔧 Environment Info")
print("=" * 20)
print(f"FLOX_ENV: {os.getenv('FLOX_ENV', 'Not set')}")
print(f"FLOX_ENV_NAME: {os.getenv('FLOX_ENV_NAME', 'Not set')}")
print(f"FLOX_ENV_PROJECT: {os.getenv('FLOX_ENV_PROJECT', 'Not set')}")

print("\n📁 Current Directory")
print("=" * 20)
print(f"Current dir: {os.getcwd()}")
print(f"Backend dir exists: {os.path.exists('backend')}")
print(f"Requirements file exists: {os.path.exists('backend/requirements.txt')}")

if os.path.exists('backend/requirements.txt'):
    print("\n📋 Requirements.txt contents:")
    with open('backend/requirements.txt', 'r') as f:
        print(f.read())
