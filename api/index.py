import os
import sys

# Ensure the root directory is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.web.cli import main

def handler(request, response):
    """
    Vercel serverless entrypoint for Streamlit.
    """
    sys.argv = [
        "streamlit", 
        "run", 
        "main.py", 
        "--server.port=3000", 
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ]
    main()

app = handler