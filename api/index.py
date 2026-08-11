import os
import sys

# Add project root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(environ, start_response):
    """
    Standard WSGI entrypoint for Vercel Serverless Python Functions.
    Exposes top-level app and handler objects expected by Vercel's build engine.
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    response_body = (
        "<html><body>"
        "<h1>🌿 Ayurveda Setu Web Service</h1>"
        "<p>The Vercel Serverless function endpoint is active.</p>"
        "</body></html>"
    )
    
    return [response_body.encode('utf-8')]

# Top-level exports for Vercel runtime detection
app = handler