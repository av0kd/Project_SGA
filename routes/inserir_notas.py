from flask import Blueprint, render_template, request
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina
from sqlalchemy.orm import joinedload

inserir_notas_bp = Blueprint('inserir_notas', __name__)

@inserir_notas_bp.route('/inserir_notas', methods=['GET','POST'])
def inserir_notas():
    if request.method == 'POST':
        matricula_aluno = request.form.get('matricula_aluno')
        aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()

        if not aluno:
            return "Aluno não encontrado", 404

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

        # Agora, carregamos as disciplinas do aluno via AlunoDisciplina
        aluno_disciplinas = AlunoDisciplina.query.filter_by(aluno_id=aluno.id).all()

        return render_template('inserir_notas.html', aluno=aluno, disciplinas=aluno_disciplinas)

    return render_template('inserir_notas.html', aluno=None)