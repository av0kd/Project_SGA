from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

vincular_disciplina_bp = Blueprint('vincular_disciplina', __name__)
disciplina_vinculada_bp = Blueprint('disciplina_vinculada', __name__)

@vincular_disciplina_bp.route('/vincular_disciplina', methods=['GET', 'POST'])
@login_required
def vincular_disciplina():
    return render_template('vincular_disciplina.html')

@disciplina_vinculada_bp.route('/disciplina_vinculada', methods=['POST'])
@login_required
def disciplina_vinculada():
    matricula_aluno = request.form.get('matricula_aluno')
    disciplina_id = request.form.get('disciplina_id')

    # Buscar o aluno pela matricula e disciplina pelo ID
    aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()
    disciplina = Disciplina.query.get(disciplina_id)

    if not aluno:
        return render_template("/400.html")
    if not disciplina:
        return render_template("/400.html")

    # Verifica se o aluno já está vinculado à disciplina
    if AlunoDisciplina.query.filter_by(aluno_id=aluno.id, disciplina_id=disciplina.id).first():
        return "O aluno já está vinculado a essa disciplina!", 400

    # Criar o vínculo entre aluno e disciplina
    novo_vinculo = AlunoDisciplina(aluno_id=aluno.id, disciplina_id=disciplina.id)
    db.session.add(novo_vinculo)
    db.session.commit()

    return "Aluno vinculado a disciplina com sucesso!"