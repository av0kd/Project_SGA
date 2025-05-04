from flask import Blueprint
from flask import redirect, url_for
from flask_login import login_required, logout_user

logout_user_bp = Blueprint('logout_user', __name__)

@logout_user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))