from flask import Flask, render_template
from models import db, Turma, Aluno, Disciplina, Nota


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)