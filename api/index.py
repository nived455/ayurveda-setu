import os
import sys
from streamlit.web import cli as stcli

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(request, response):
    sys.argv = ["streamlit", "run", "main.py", "--server.port=3000", "--server.address=0.0.0.0"]
    stcli.main()