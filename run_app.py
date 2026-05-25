import subprocess
import sys
import os

def main():
    script_path = os.path.join(os.path.dirname(__file__), "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", script_path, "--browser.serverAddress=localhost", "--server.headless=true"])

if __name__ == "__main__":
    main()