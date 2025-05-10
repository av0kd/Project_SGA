from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, Usuario
from blueprints import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'projetograu'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login' 
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

register_blueprints(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        matricula_user = request.form['matricula_user']
        senha_user = request.form['senha_user']

        user = Usuario.query.filter_by(matricula_user=matricula_user, senha_user=senha_user).first()

        if not user:
            return f'Matricula ou senha incorretos!!'

        login_user(user)
        return redirect(url_for('index.index'))

if __name__ == '__main__':
    app.run(debug=True)
