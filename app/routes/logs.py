import logging
logger = logging.getLogger()

import json
import os

import hashlib

from flask import Blueprint, jsonify, request, render_template

from functools import wraps
from flask import session, redirect
from collections import deque

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/admin/auth")
        return f(*args, **kwargs)
    return wrapper

logs_bp = Blueprint("logs", __name__)


LOGGING_DIR = "./app/logging/"

LOG_FILE = LOGGING_DIR + "logs/app.log"
PASS_FILE = LOGGING_DIR + "auth/creds.txt"

@logs_bp.route("/logs")
@admin_required
def get_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify({"error": "Log file not found"}), 404

    level = request.args.get("level")
    search = request.args.get("search")

    logs = []
    with open(LOG_FILE, "r") as f:
        for line in deque(f, maxlen=200):
            try:
                log = json.loads(line)
            except:
                continue

            if level and log.get("levelname") != level:
                continue

            if search and search.lower() not in str(log).lower():
                continue

            logs.append(log)

    return jsonify(logs)

@logs_bp.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/auth")
