import socket
import subprocess
import sys
import os

def find_free_port(start_port=8501, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def main():
    print("🚀 Starting AI Text Humanizer Pro...")
    print("🔍 Looking for available port...")
    
    # Find a free port
    port = find_free_port()
    
    if port is None:
        print("❌ Could not find an available port. Please close other applications and try again.")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Found available port: {port}")
    print(f"🌐 App will open at: http://localhost:{port}")
    print("=" * 50)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "modern_humanizer.py", 
            "--server.port", str(port),
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()




