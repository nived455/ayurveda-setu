def handler(request, response):
    """
    Standard HTTP Request Handler for Vercel Serverless Functions
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "<h1>🌿 Ayurveda Setu Backend Active</h1>"
    }

# Expose app at top level for Vercel discovery
app = handler