from flask import Flask, render_template, request, send_file
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina
from blueprints import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

register_blueprints(app)

@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)