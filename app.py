"""CLI entry point; launches the Streamlit user interface."""
import subprocess
import sys

if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, "-m", "streamlit", "run", "web_app.py"]))
