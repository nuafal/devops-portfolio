from flask import Flask, render_template_string
import redis
import os
import socket
import datetime

app = Flask(__name__)

# CONNECT TO REDIS
redis_host = os.getenv('REDIS_HOST', 'redis-service')
cache = redis.Redis(host=redis_host, port=6379)

# THE DASHBOARD HTML (Now inside Python!)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Master | Naufal</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: #1e293b; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); width: 350px; text-align: center; border: 1px solid #334155; }
        .metric { font-size: 4rem; font-weight: bold; color: #22c55e; margin: 1rem 0; text-shadow: 0 0 20px rgba(34,197,94,0.5); }
        .label { color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem; }
        .footer { margin-top: 1.5rem; font-size: 0.7rem; color: #64748b; }
        .pod-id { color: #f59e0b; }
    </style>
</head>
<body>
    <div class="card">
        <div class="label">Total Visitors (Redis)</div>
        <div class="metric">{{ count }}</div>
        <div class="label">Served By Pod</div>
        <div class="footer">
            ID: <span class="pod-id">{{ hostname }}</span><br>
            Time: {{ time }}
        </div>
    </div>
    <script>
        // Auto-refresh every 2 seconds to see load balancing!
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

@app.route('/')
def hello():
    count = get_hit_count()
    hostname = socket.gethostname()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return render_template_string(HTML_TEMPLATE, count=count, hostname=hostname, time=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)