from flask import Blueprint, render_template, session, jsonify
from flask_login import login_required
import psutil

metrics_bp = Blueprint("metrics", __name__)


def get_system_metrics():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_used": mem.used / (1024**3),      # GB
        "memory_total": mem.total / (1024**3),
        "memory_percent": mem.percent,
        "disk_used": disk.used / (1024**3),
        "disk_total": disk.total / (1024**3),
        "disk_percent": disk.percent
    }

@metrics_bp.route("/metrics")
@login_required
def metrics_page():        
    metrics = get_system_metrics()
    return render_template("metrics/metrics.html", metrics=metrics)


@metrics_bp.route("/metrics-json")
@login_required
def metrics_json():
    return jsonify(get_system_metrics())
