from flask import Blueprint, render_template, request
from flask_login import login_required
from models import db, Turma, Aluno, Disciplina, Nota,  AlunoDisciplina

cadastrar_disciplinas_bp = Blueprint('cadastrar_disciplinas', __name__)
disciplina_cadastrada_bp = Blueprint('disciplina_cadastrada', __name__)
consultar_disciplina_bp = Blueprint('consultar_disciplina', __name__)
disciplina_consultada_bp = Blueprint('disciplina_consultada', __name__)
deletar_disciplina_bp = Blueprint('deletar_disciplina', __name__)
disciplina_deletada_bp = Blueprint('disciplina_deletada', __name__)

@cadastrar_disciplinas_bp.route('/cadastrar_disciplinas')
@login_required
def cadastrar_disciplinas():
    return render_template('cadastrar_disciplinas.html')

@disciplina_cadastrada_bp.route('/disciplina_cadastrada', methods=['POST'])
@login_required
def disciplina_cadastrada():
    nome_disciplina = request.form.get('nome_disciplina')

    nova_disciplina = Disciplina(nome=nome_disciplina)
    db.session.add(nova_disciplina)
    db.session.commit()
    return render_template('disciplina_cadastrada.html', disciplina = nova_disciplina)

@consultar_disciplina_bp.route('/consultar_disciplina')
@login_required
def consultar_disciplina():
    return render_template('consultar_disciplina.html')

@disciplina_consultada_bp.route('/disciplina_consultada', methods=['POST'])
@login_required
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

@deletar_disciplina_bp.route('/deletar_disciplina')
@login_required
def deletar_disciplina():
    return render_template('deletar_disciplina.html')

@disciplina_deletada_bp.route('/disciplina_deletada', methods = ['POST'])
@login_required
def disciplina_deletada():
    nome_disciplina = request.form.get('nome_disciplina')

    if not nome_disciplina:
        return render_template('400.html', mensagem = "Nome da disciplina obrigatório")
    
    disciplina = Disciplina.query.filter_by(disciplina = nome_disciplina).first()

    if not disciplina:
        return render_template('404.html', mensagem="Disciplina não encontrada.")

    db.session.delete(disciplina)
    db.session.commit()

    return render_template('disciplina_deletada.html')