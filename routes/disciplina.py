from flask import Blueprint, render_template, request
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

cadastrar_disciplinas_bp = Blueprint('cadastrar_disciplinas', __name__)
disciplina_cadastrada_bp = Blueprint('disciplina_cadastrada', __name__)
consultar_disciplina_bp = Blueprint('consultar_disciplina', __name__)
disciplina_consultada_bp = Blueprint('disciplina_consultada', __name__)

@cadastrar_disciplinas_bp.route('/cadastrar_disciplinas')
def cadastrar_disciplinas():
    return render_template('cadastrar_disciplinas.html')

@disciplina_cadastrada_bp.route('/disciplina_cadastrada', methods=['POST'])
def disciplina_cadastrada():
    nome_disciplina = request.form.get('nome_disciplina')

    nova_disciplina = Disciplina(nome=nome_disciplina)
    db.session.add(nova_disciplina)
    db.session.commit()
    return render_template('disciplina_cadastrada.html', disciplina = nova_disciplina)

@consultar_disciplina_bp.route('/consultar_disciplina')
def consultar_disciplina():
    return render_template('consultar_disciplina.html')

@disciplina_consultada_bp.route('/disciplina_consultada', methods=['POST'])
def disciplina_consultada():
    nome_disciplina = request.form.get('nome_disciplina')

    if not nome_disciplina:
        disciplinas = Disciplina.query.all()

        if not disciplinas:
            return "Nenhuma disciplina cadastrada.", 404

        return render_template('disciplina_consultada.html', disciplinas=disciplinas, mostrar_todas=True)

    disciplina = Disciplina.query.filter_by(nome=nome_disciplina).first()

    if not disciplina:
        return f"Disciplina '{nome_disciplina}' não encontrada.", 404

    alunos = Aluno.query.join(AlunoDisciplina).filter(AlunoDisciplina.disciplina_id == disciplina.id).all()

    return render_template('disciplina_consultada.html', disciplina=disciplina, alunos=alunos, disciplina_id=disciplina.id)

