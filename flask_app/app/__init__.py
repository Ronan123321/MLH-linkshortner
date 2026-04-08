import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from app.database import db, init_db
from app.models import product
from app.models.events import Events
from app.models.urls import Urls
from app.models.users import Users
from app.models.susers import Susers
from app.auth.seed import seed_admin
from app.routes import register_routes

from app.auth.manager import login_manager

from prometheus_flask_exporter import PrometheusMetrics


def create_app(is_pytest=False):
    load_dotenv()

    app = Flask(__name__)

    # Added by ronan for his logs endpoint auth
    app.secret_key = "mylittlesecret"
    login_manager.init_app(app)
    # Added by ronan for his metrics
    metrics = PrometheusMetrics(app)


    init_db(app)

    if os.environ.get("DEBUG_PROFILE", "false") == "true":
        from werkzeug.middleware.profiler import ProfilerMiddleware

        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app,
            restrictions=[30],
            profile_dir="/app/profiler",
            filename_format="{method}-{path}-{time:.0f}-{elapsed:.0f}ms.prof",
        )

    from app import models  # noqa: F401 - registers models with Peewee

    if not is_pytest:
        db.create_tables([Users, Events, Urls, Susers], safe=True)
        seed_admin()

    register_routes(app)

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    return app
