import time
import redis
import socket
import datetime
from flask import Flask, render_template_string

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# ---------------------------------------------------
#  HTML TEMPLATE (The User Interface)
# ---------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My DevOps Project</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background-color: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; width: 400px; }
        h1 { color: #007bff; margin-bottom: 10px; }
        .counter { font-size: 64px; font-weight: bold; color: #333; margin: 20px 0; }
        .footer { color: #666; font-size: 14px; margin-top: 20px; }
        .tag { background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Version 2: CI/CD Live!</h1>
        <p>This page was updated automatically by GitHub Actions.</p>
        
        <div class="counter">{{ count }}</div>
        <p>Total Visits</p>
        
        <div class="footer">
            Served by Container ID: <br>
            <code>{{ hostname }}</code>
        </div>
    </div>

    <script>
        setTimeout(() => window.location.reload(), 2000);
    </script>
</body>
</html>
"""

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    try:
        count = get_hit_count()
    except:
        count = "Redis Offline"
        
    hostname = socket.gethostname()
    return render_template_string(HTML_TEMPLATE, count=count, hostname=hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
