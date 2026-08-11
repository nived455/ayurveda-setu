import os
import sys

# Get absolute path to the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure root directory is at the front of sys.path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Change working directory to root so relative file paths (like data/ayurveda_data.json) resolve properly
os.chdir(ROOT_DIR)

# WSGI Handler for Vercel
def app(environ, start_response):
    data = b"Vercel Python backend is active."
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])