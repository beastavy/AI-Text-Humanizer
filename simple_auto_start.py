#!/usr/bin/env python3
"""
Simple Auto-start AI Text Humanizer - just finds available port
"""
import socket
import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def find_free_port(start_port=8501, max_attempts=20):
    """Find a free port starting from start_port"""
    print("🔍 Searching for available port..."    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            print(f"   Port {port}: ❌ Busy")
            continue
    return None

def main():
    print("🚀 AI Text Humanizer Pro - Simple Auto Start")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("modern_humanizer.py").exists():
        print("❌ modern_humanizer.py not found in current directory")
        print("Please run this script from the AI-Text-Humanizer-App directory")
        input("Press Enter to exit...")
        return

    # Find available port
    port = find_free_port()

    if port is None:
        print("❌ Could not find an available port after checking 8501-8520")
        print("Please close some applications and try again")
        print("💡 Try closing browser tabs or other Streamlit apps")
        input("Press Enter to exit...")
        return

    print(f"✅ Found available port: {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print("=" * 50)

    # Start Streamlit
    url = f"http://localhost:{port}"

    try:
        print("🎯 Starting Streamlit server...")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            "modern_humanizer.py",
            "--server.port", str(port),
            "--server.headless", "true",
            "--theme.base", "light"
        ])

        print("✅ Server started successfully!")
        print("⏳ Waiting for server to be ready...")
        time.sleep(3)

        # Open browser
        print(f"🌐 Opening browser: {url}")
        webbrowser.open(url)

        print("✅ App is ready!")
        print("=" * 50)
        print("INSTRUCTIONS:")
        print(f"📱 Your app is running at: {url}")
        print("🔄 To restart: Close this window and run again")
        print("❌ To stop: Close this terminal window")
        print("=" * 50)

        # Keep the script running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("👋 Server stopped")

    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()




