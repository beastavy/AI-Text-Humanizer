#!/usr/bin/env python3
"""
Auto-start AI Text Humanizer with automatic port detection
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

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                connections = proc.info.get('connections', [])
                for conn in connections:
                    if hasattr(conn, 'laddr') and conn.laddr[1] == port:
                        print(f"🛑 Killing process {proc.info['pid']} using port {port}")
                        proc.terminate()
                        proc.wait(timeout=5)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except ImportError:
        print("   ⚠️  psutil not available, skipping process cleanup")

    return False

def main():
    print("🚀 AI Text Humanizer Pro - Auto Start")
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

        # Try to kill processes on common ports
        print("🛑 Attempting to free up common ports...")
        for p in [8501, 8502, 8503, 8500]:
            if kill_process_on_port(p):
                print(f"✅ Port {p} freed up")
                port = p
                break

        if port is None:
            input("Press Enter to exit...")
            return

    print(f"✅ Using port: {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print("=" * 50)

    # Wait a moment for port cleanup
    time.sleep(1)

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
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("✅ Server started successfully!")

        # Wait for server to be ready
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
        print("❌ To stop: Press Ctrl+C or close this terminal")
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




