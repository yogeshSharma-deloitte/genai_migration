# Number of worker processes
workers = 4

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"  # You can change this to other async worker classes if needed

# Bind address and port
bind = "0.0.0.0:8000"

# Maximum requests per worker
max_requests = 1000
# Timeout for graceful worker shutdown
graceful_timeout = 1200
timeout = 1200

# Keep-alive connections
keepalive = 5

# Preload the application before forking worker processes
preload_app = True
