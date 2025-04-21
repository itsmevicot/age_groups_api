import signal
import subprocess
import sys

procs = []

def _terminate(signum, frame):
    for p in procs:
        p.send_signal(signal.SIGINT)
    sys.exit(0)

signal.signal(signal.SIGINT, _terminate)
signal.signal(signal.SIGTERM, _terminate)

procs.append(
    subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=sys.stdout, stderr=sys.stderr
    )
)

procs.append(
    subprocess.Popen(
        ["python", "processor/worker.py"],
        stdout=sys.stdout, stderr=sys.stderr
    )
)

for p in procs:
    p.wait()
