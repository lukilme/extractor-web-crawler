from celery import Celery
from pymongo import MongoClient
import os
import uuid
import tempfile
import shutil
import subprocess

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client_mongo = MongoClient(MONGO_URL)
db = client_mongo["appdb"]
scripts = db["scripts"]

celery = Celery("app")
celery.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    task_serializer="json",
    accept_content=["json"],
)

@celery.task(bind=True)
def run_script_task(self, script_id, params=None):
    doc = scripts.find_one({"_id": script_id})
    if not doc:
        raise ValueError("Script não encontrado")

    code = doc["code"]

    workdir = tempfile.mkdtemp(prefix="script-run-")
    try:
        script_path = os.path.join(workdir, "script.py")
        with open(script_path, "w") as f:
            f.write(code)

        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", "256m",
            "--cpus", "0.5",
            "-v", f"{workdir}:/work:ro",
            "-w", "/work",
            "python:3.11-slim",
            "timeout", "30s", "python", "script.py"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=40
        )

        logs = (result.stdout or "") + (result.stderr or "")
        exit_code = result.returncode

        scripts.update_one(
            {"_id": script_id},
            {"$set": {"last_run": {"exit_code": exit_code, "logs": logs}}}
        )

        return {"exit_code": exit_code, "logs": logs}

    finally:
        shutil.rmtree(workdir, ignore_errors=True)
