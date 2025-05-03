from flask import Blueprint, render_template, request
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

criar_turmas_bp = Blueprint('criar_turmas', __name__)
turmas_criadas_bp = Blueprint('turmas_criadas', __name__)
pesquisar_turmas_bp = Blueprint('pesquisar_turmas', __name__)
turmas_pesquisadas_bp = Blueprint('turmas_pesquisadas', __name__)
deletar_turmas_bp = Blueprint('deletar_turmas', __name__)
turmas_deletadas_bp = Blueprint('turmas_deletadas', __name__)

@criar_turmas_bp.route('/criar_turmas')
def criar_turmas():
    return render_template('criar_turmas.html')

@turmas_criadas_bp.route('/turmas_criadas', methods =['POST'])
def turmas_criadas():
    nome_turma = request.form.get('nome_turma')

    if not nome_turma:
        return render_template('400.html')

    nova_turma = Turma(nome=nome_turma)
    db.session.add(nova_turma)
    db.session.commit()

    return render_template('turmas_criadas.html', turma=nova_turma)

@pesquisar_turmas_bp.route('/pesquisar_turmas')
def pesquisar_turmas():
    return render_template('pesquisar_turmas.html')

@turmas_pesquisadas_bp.route('/turmas_pesquisadas', methods=['POST'])
def turmas_pesquisadas():
    nome_turma = request.form.get('nome_turma', '').strip()  # Obtém o nome e remove espaços extras

    if nome_turma:  
        # Filtra as turmas pelo nome informado
        turmas = Turma.query.filter(Turma.nome.ilike(f"%{nome_turma}%")).all()
    else:
        # Se não houver nome informado, retorna todas as turmas
        turmas = Turma.query.all()

    if not turmas:
        return render_template('400.html')

    return render_template('turmas_pesquisadas.html', turmas=turmas)

@deletar_turmas_bp.route('/deletar_turma', methods=['GET'])
def deletar_turma():
    return render_template('deletar_turma.html')

@turmas_deletadas_bp.route('/turma_deletada', methods=['POST'])
def turma_deletada():
    if request.method == "POST":
        turma_id = request.form.get("turma_id")

        if not turma_id:
            return render_template('400.html')

        turma = Turma.query.get(turma_id)

        if not turma:
            return render_template('400.html')

        db.session.delete(turma)
        db.session.commit()

        return render_template('/turma_deletada.html')