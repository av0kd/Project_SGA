from flask import Flask, render_template, request
from models import db, Turma, Aluno, Disciplina, Nota


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def inicio():
    return render_template('index.html')

#Rotas para gerenciar a parte dos alunos
@app.route('/adicionar_alunos')
def adicionar_alunos():
    return render_template('adicionar_alunos.html')

@app.route('/alunos_adicionados', methods=["POST"])
def alunos_adicionados():
    nome = request.form.get('nome')
    matricula = request.form.get('matricula')
    turma_id = request.form.get('turma_id')

    novo_aluno = Aluno(nome=nome, matricula=matricula, turma_id=turma_id)
    db.session.add(novo_aluno)
    db.session.commit()
    return render_template('alunos_adicionados.html')

#Rotas para gerenciar a parte das turmas
@app.route('/criar_turmas')
def criar_turmas():
    return render_template('criar_turmas.html')

@app.route('/turmas_criadas', methods=["POST"])
def turmas_criadas():
    nome_turma = request.form.get('nome_turma')

    # Verificação simples para evitar turmas sem nome
    if not nome_turma:
        return "Erro: Nome da turma é obrigatório.", 400

    # Criação da nova turma
    nova_turma = Turma(nome=nome_turma)
    db.session.add(nova_turma)
    db.session.commit()

    return render_template('turmas_criadas.html', turma=nova_turma)

if __name__ == '__main__':
    app.run(debug=True)