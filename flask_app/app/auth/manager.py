from flask_login import LoginManager

from app.models.susers import Susers

login_manager = LoginManager()
login_manager.login_view = "auth.admin_login"
@login_manager.user_loader
def load_user(user_id):
    return Susers.get_by_id(user_id)
