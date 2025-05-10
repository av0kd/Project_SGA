from flask import Blueprint, render_template, request
from models import db, Aluno, Disciplina, Nota
from flask_login import login_required
from sqlalchemy.orm import joinedload

inserir_notas_bp = Blueprint('inserir_notas', __name__)

@inserir_notas_bp.route('/inserir_notas', methods=['GET', 'POST'])
@login_required
def inserir_notas():
    if request.method == 'POST':
        matricula_aluno = request.form.get('matricula_aluno')
        aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()

        if not aluno:
            return "Aluno não encontrado", 404

        # Agora você busca as disciplinas associadas à turma do aluno
        turma = aluno.turma  # Assumindo que o aluno tenha uma relação com a turma
        disciplinas_associadas = turma.disciplinas  # Disciplinas da turma do aluno

        notas_enviadas = {key: value for key, value in request.form.items() if key.startswith('nota_')}
        
        if notas_enviadas:
            for key, valor_nota in notas_enviadas.items():
                disciplina_id = int(key.split('_')[1])
                valor_nota = float(valor_nota)

                nota_existente = Nota.query.filter_by(aluno_id=aluno.id, disciplina_id=disciplina_id).first()

                if nota_existente:
                    nota_existente.valor = valor_nota
                else:
                    nova_nota = Nota(aluno_id=aluno.id, disciplina_id=disciplina_id, valor=valor_nota)
                    db.session.add(nova_nota)

            db.session.commit()

        # Retorna apenas as disciplinas associadas à turma
        return render_template('inserir_notas.html', aluno=aluno, disciplinas=disciplinas_associadas)

    return render_template('inserir_notas.html', aluno=None)
