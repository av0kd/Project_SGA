from flask import Flask, render_template, request, send_file
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina


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

@app.route('/pesquisar_alunos')
def pesquisar_alunos():
    return render_template('pesquisar_alunos.html')

@app.route('/aluno_pesquisado', methods=['POST'])
def aluno_pesquisado():
    aluno_nome = request.form.get('nome_aluno')

    if not aluno_nome:
        return "Erro: nome do aluno é obrigatório", 400

    # Consulta o nome do aluno, turma e matricula
    resultado_query = db.session.query(Aluno.nome, Aluno.matricula, Turma.nome) \
    .join(Turma, Aluno.turma_id == Turma.id) \
    .filter(Aluno.nome == aluno_nome) \
    .all() 

    if not resultado_query:
        return f"Nenhum aluno encontrado com o nome: {aluno_nome}"

    return render_template('aluno_pesquisado.html', resultado_query=resultado_query)

@app.route('/editar_aluno')
def editar_aluno():
    return render_template('editar_aluno.html')

@app.route('/aluno_editado', methods = ["POST"])
def aluno_editado():
    matricula = request.form.get('matricula')
    novo_nome = request.form.get('nome_aluno')
    nova_turma_id = request.form.get('id_turma')

    # Verificar se a matrícula foi fornecida
    if not matricula:
        return "Erro: a matrícula do aluno é obrigatória.", 400

    aluno = Aluno.query.filter_by(matricula=matricula).first()

    if not aluno:
        return f"Aluno com matrícula '{matricula}' não encontrado.", 404

    # Atualizar os dados do aluno se fornecidos
    if novo_nome:
        aluno.nome = novo_nome

    if nova_turma_id:
        aluno.turma_id = nova_turma_id

    db.session.commit()
    
    return render_template('aluno_editado.html', aluno=aluno)

@app.route('/deletar_aluno')
def deletar_aluno():
    return render_template('deletar_aluno.html')

@app.route('/aluno_deletado', methods = ["POST"])
def aluno_deletado():
    matricula_aluno = request.form.get('matricula_aluno')

    if not matricula_aluno:
        return "Erro: matrícula do aluno é obrigatória.", 400
    
    aluno = Aluno.query.filter_by(matricula = matricula_aluno).first()

    if not aluno:
        return f"Nenhum aluno encontrado com a matrícula '{matricula_aluno}'.", 404

    db.session.delete(aluno)
    db.session.commit()

    return render_template('aluno_deletado.html', nome_aluno=aluno.nome, matricula_aluno=aluno.matricula)

#<------------------AQUI ENCERRA A PARTE DO CRUD DOS ALUNOS------------------>

#Rotas para gerenciar a parte das turmas
@app.route('/criar_turmas')
def criar_turmas():
    return render_template('criar_turmas.html')

@app.route('/turmas_criadas', methods=["POST"])
def turmas_criadas():
    nome_turma = request.form.get('nome_turma')

    if not nome_turma:
        return "Erro: Nome da turma é obrigatório", 400

    nova_turma = Turma(nome=nome_turma)
    db.session.add(nova_turma)
    db.session.commit()

    return render_template('turmas_criadas.html', turma=nova_turma)

@app.route('/pesquisar_turmas')
def pesquisar_turmas():
    return render_template('pesquisar_turmas.html')

@app.route('/turmas_pesquisadas', methods = ["POST"])
def turmas_pesquisadas():
    turmas = Turma.query.all()

    if not turmas:
        return "Nenhuma turma encontrada", 400

    return render_template('turmas_pesquisadas.html', turmas=turmas)

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

@app.route('/vincular_disciplina')
def vincular_disciplina():
    return render_template('vincular_disciplina.html')

@app.route('/disciplina_vinculada', methods=['POST'])
def disciplina_vinculada():
    matricula_aluno = request.form.get('matricula_aluno')
    disciplina_id = request.form.get('disciplina_id')

    # Buscar o aluno pela matricula e disciplina pelo ID
    aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()
    disciplina = Disciplina.query.get(disciplina_id)

    if not aluno:
        return "Aluno não encontrado", 404
    if not disciplina:
        return "Disciplina não encontrada", 404

    # Vincular o aluno a disciplina
    aluno_disciplina = AlunoDisciplina(aluno_id=aluno.id, disciplina_id=disciplina.id)
    db.session.add(aluno_disciplina)
    db.session.commit()

    disciplinas = Disciplina.query.all()
    return render_template('disciplina_vinculada.html', disciplinas=disciplinas)

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