# A standard WSGI application that Vercel's Python runtime requires
def app(environ, start_response):
    data = b"Vercel Python backend is successfully deployed."
    
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    
    return iter([data])