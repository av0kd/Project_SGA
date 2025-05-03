from flask import Blueprint, render_template, request
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

adicionar_alunos_bp = Blueprint('adicionar_alunos', __name__)
alunos_adicionados_bp = Blueprint('alunos_adicionados', __name__)
pesquisar_alunos_bp = Blueprint('pesquisar_alunos', __name__)
aluno_pesquisado_bp = Blueprint('aluno_pesquisado', __name__)
editar_alunos_bp = Blueprint('editar_alunos', __name__)
aluno_editado_bp = Blueprint('aluno_editado', __name__)
deletar_aluno_bp = Blueprint('deletar_aluno', __name__)
aluno_deletado_bp = Blueprint('aluno_deletado', __name__)

@adicionar_alunos_bp.route('/adicionar_alunos')
def adicionar_alunos():
    return render_template('adicionar_alunos.html')

@alunos_adicionados_bp.route('/alunos_adicionados', methods=['POST'])
def alunos_adicionados():
    nome = request.form.get('nome')
    matricula = request.form.get('matricula')
    turma_id = request.form.get('turma_id')

    novo_aluno = Aluno(nome=nome, matricula=matricula, turma_id=turma_id)
    db.session.add(novo_aluno)
    db.session.commit()
    return render_template('alunos_adicionados.html')

#--------------------------------------------------------------
    
@pesquisar_alunos_bp.route('/pesquisar_alunos')
def pesquisar_alunos():
    return render_template('pesquisar_alunos.html')

@aluno_pesquisado_bp.route('/aluno_pesquisado', methods=['POST'])
def aluno_pesquisado():
    aluno_nome = request.form.get('nome_aluno')

    # Se o nome do aluno não for fornecido, mostrar todos os alunos
    if not aluno_nome:
        resultado_query = db.session.query(Aluno.nome, Aluno.matricula, Turma.nome) \
            .outerjoin(Turma, Aluno.turma_id == Turma.id) \
            .all()
    else:
        # Caso o nome do aluno seja fornecido, filtra pelo nome
        resultado_query = db.session.query(Aluno.nome, Aluno.matricula, Turma.nome) \
            .outerjoin(Turma, Aluno.turma_id == Turma.id) \
            .filter(Aluno.nome == aluno_nome) \
            .all()

    # Verifica se a consulta retornou algum aluno
    if not resultado_query:
        return f"Nenhum aluno encontrado com o nome: {aluno_nome}" if aluno_nome else "Nenhum aluno encontrado"

    return render_template('aluno_pesquisado.html', resultado_query=resultado_query)

@editar_alunos_bp.route('/editar_aluno')
def editar_aluno():
    return render_template('editar_aluno.html')

@aluno_editado_bp.route('/aluno_editado', methods = ["POST"])
def aluno_editado():
    matricula = request.form.get('matricula')
    novo_nome = request.form.get('nome_aluno')
    nova_turma_id = request.form.get('id_turma')

    # Verificar se a matrícula foi fornecida
    if not matricula:
        return render_template("404.html")

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

@deletar_aluno_bp.route('/deletar_aluno')
def deletar_aluno():
    return render_template('deletar_aluno.html')

@aluno_deletado_bp.route('/aluno_deletado', methods=['POST'])
def aluno_deletado():
    matricula_aluno = request.form.get('matricula_aluno')

    if not matricula_aluno:
        return "Erro: matrícula do aluno é obrigatória.", 400

    aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()

    if not aluno:
        return f"Nenhum aluno encontrado com a matrícula '{matricula_aluno}'.", 404

    # Remover todas as notas associadas ao aluno
    Nota.query.filter_by(aluno_id=aluno.id).delete()

    # Remover registros da tabela intermediária AlunoDisciplina
    AlunoDisciplina.query.filter_by(aluno_id=aluno.id).delete()

    # Deletar o próprio aluno
    db.session.delete(aluno)
    db.session.commit()

    return render_template('aluno_deletado.html', nome_aluno=aluno.nome, matricula_aluno=aluno.matricula)
