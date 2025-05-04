from flask import Blueprint, render_template, request, redirect, url_for
from models import Usuario, db

register_user_bp = Blueprint('register_user', __name__)

@register_user_bp.route('/register_user', methods=['POST', 'GET'])
def register_user():
    if request.method == 'GET':
        return render_template('register_user.html')

    elif request.method == 'POST':
        matricula_user = request.form['matricula_user']
        senha_user = request.form['senha_user']
        cargo = request.form['cargo_user']
        nome_user = request.form['nome_user']

        novo_user = Usuario(matricula_user = matricula_user, senha_user = senha_user, cargo = cargo, nome_user = nome_user)
        db.session.add(novo_user)
        db.session.commit()

        return redirect(url_for('/'))