import subprocess
import time

import requests
from invoke import task


@task
def docs(c):
    # Start Django dev server
    server = subprocess.Popen(
        ["poetry", "run", "python", "manage.py", "runserver", "8001"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    try:
        # Wait for the server to start
        for _ in range(20):
            try:
                resp = requests.get("http://localhost:8001/")
                if resp.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            print("Django server did not start in time.")
            server.terminate()
            return

        # Run shot-scraper
        c.run("shot-scraper html http://localhost:8001/ -o docs/index.html")
    finally:
        server.terminate()
        server.wait()
