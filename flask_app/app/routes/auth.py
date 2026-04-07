import logging
logger = logging.getLogger(__name__)

import hashlib
import json
from collections import deque

from flask import Blueprint, render_template, redirect, request, jsonify, session
from flask_login import login_user, login_required

from app.models.susers import Susers


auth_bp = Blueprint("auth", __name__)


def verify_creds(user, password):
    password = password.strip()
    password = hashlib.sha256(password.encode()).hexdigest()
    try:
        hash = user.password
    except Exception as e:
        logger.exceptions("There was a problem fetching credentials from susers database", extra={"Exception": e})
        return jsonify({"error": "Error: There was a problem fetching credentials"}), 500
    logger.info("Creds retrieved and ready to verify",
                extra={
                    "username": user,
                    "password": password,
                    "hash:": hash
                })

    return hash == password

@auth_bp.route("/admin/auth", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user =Susers.get_or_none(Susers.username == username)
        except Exception as e:
            logger.exception("There was a problem retreiving the user",
                             extra={
                                 "username:": username,
                                 "password:": password
                             })
            return jsonify({"error": "Error: THere was a problem fetching the user"}), 500

        if user is None:
            return render_template("auth/auth.html", error="Invalid Credentails")

        if verify_creds(user, password):
            login_user(user)
            return redirect("/admin/logs")
        else:
            return render_template("auth/auth.html", error="Invalide Credentials")
        
    return render_template("auth/auth.html")
        
@auth_bp.route("/admin/logs")
@login_required
def admin_dash():
    return render_template("logs/logs.html")
    
@auth_bp.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/auth")
