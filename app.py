from flask import Flask, render_template, request, send_file
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

    if not nome_turma:
        return "Erro: Nome da turma é obrigatório.", 400

    nova_turma = Turma(nome=nome_turma)
    db.session.add(nova_turma)
    db.session.commit()

    return render_template('turmas_criadas.html', turma=nova_turma)

#Rotas para disciplinas
@app.route('/cadastrar_disciplinas')
def cadastrar_disciplinas():
    return render_template('cadastrar_disciplinas.html')

@app.route('/disciplina_cadastrada', methods = ["POST"])
def disciplina_cadastrada():
    nome_disciplina = request.form.get('nome_disciplina')

    nova_disciplina = Disciplina(nome=nome_disciplina)
    db.session.add(nova_disciplina)
    db.session.commit()
    return render_template('disciplina_cadastrada.html', disciplina = nova_disciplina)

#Rota para criar o relatório das notas do aluno
@app.route('/gerar_relatorio', methods=['POST'])
def gerar_relatorio():
    nome_aluno = request.form.get('nome_aluno')

    resultado = db.session.query(
        Aluno.nome, Turma.nome, Disciplina.nome, Nota.valor
    ).join(Turma, Aluno.turma_id == Turma.id) \
     .join(Nota, Nota.aluno_id == Aluno.id) \
     .join(Disciplina, Nota.disciplina_id == Disciplina.id) \
     .filter(Aluno.nome.ilike(f"%{nome_aluno}%")).all()

    if not resultado:
        return "Aluno não encontrado ou sem notas cadastradas."

    nome_aluno = resultado[0][0]
    nome_turma = resultado[0][1]
    notas_disciplinas = [(disciplina, nota) for _, _, disciplina, nota in resultado]

    notas = [nota for _, nota in notas_disciplinas]
    media = sum(notas) / len(notas)

    nome_arquivo = f"relatorio_notas_{nome_aluno}.txt"

    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(f"Nome do Aluno: {nome_aluno}\n")
        arquivo.write(f"Turma: {nome_turma}\n\n")
        arquivo.write("Disciplina\tNota\n")
        for disciplina, nota in notas_disciplinas:
            arquivo.write(f"{disciplina}\t{nota}\n")
        arquivo.write(f"Média Final: {media:.2f}\n")

    return send_file(nome_arquivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)