import os
import sys

# Ensure root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def handler(environ, start_response):
    """
    WSGI handler function for Vercel Python runtime.
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Ayurveda Setu Service</title></head>
    <body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>🌿 Ayurveda Setu Web Service</h1>
        <p>Vercel Serverless Function endpoint is active.</p>
    </body>
    </html>
    """
    return [html.encode('utf-8')]

# Explicit top-level exports expected by Vercel runtime
app = handler
application = handler