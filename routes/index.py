from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

index_bp = Blueprint('index', __name__)

@index_bp.route('/index')
@login_required
def index():
    return render_template('index.html')