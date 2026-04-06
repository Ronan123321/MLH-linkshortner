import logging
logger = logging.getLogger(__name__)

import json
import os

import hashlib

from flask import Blueprint, jsonify, request, render_template
from flask import session, redirect
from flask_login import login_required

from functools import wraps
from collections import deque

from app.logging_config import LOG_DIR

logs_bp = Blueprint("logs", __name__)

LOG_FILE = "app.log"

@logs_bp.route("/logs")
@login_required
def get_logs():
    log_file = LOG_DIR / LOG_FILE
    if not log_file.exists():
        logger.debug("Attempter to find log file, but couldnt",
                     extra={"file_path:": log_file})
        return jsonify({"error": "Log file not found"}), 404

    level = request.args.get("level")
    search = request.args.get("search")

    logs = []
    with log_file.open() as f:
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
