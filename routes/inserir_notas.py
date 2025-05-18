from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Aluno, Disciplina, Nota, Turma
from flask_login import login_required
from sqlalchemy.orm import joinedload

inserir_notas_bp = Blueprint('inserir_notas', __name__)

@inserir_notas_bp.route('/inserir_notas', methods=['GET', 'POST'])
@login_required
def inserir_notas():
    turmas = Turma.query.all()
    alunos = []
    disciplinas = []
    turma_selecionada = None

    if request.method == 'POST':
        acao = request.form.get('acao')
        turma_id = request.form.get('turma_id')

        if not turma_id:
            flash('Selecione uma turma.', 'error')
            return render_template('inserir_notas.html', turmas=turmas)

        turma_selecionada = Turma.query.get(turma_id)
        if not turma_selecionada:
            flash('Turma não encontrada.', 'error')
            return render_template('inserir_notas.html', turmas=turmas)

        alunos = Aluno.query.filter_by(turma_id=turma_selecionada.id).all()
        disciplinas = turma_selecionada.disciplinas

        if acao == 'carregar':
            nota_objs = Nota.query.join(Aluno).filter(Aluno.turma_id == turma_selecionada.id).all()
            notas_dict = {(nota.aluno_id, nota.disciplina_id): nota.valor for nota in nota_objs}

            return render_template('inserir_notas.html', turmas=turmas, alunos=alunos,
                                   disciplinas=disciplinas, turma_selecionada=turma_selecionada,
                                   notas_dict=notas_dict)

        elif acao == 'salvar':
            for aluno in alunos:
                for disciplina in disciplinas:
                    campo = f'nota_{aluno.id}_{disciplina.id}'
                    valor = request.form.get(campo)
                    if valor:
                        valor_float = float(valor)
                        nota = Nota.query.filter_by(aluno_id=aluno.id, disciplina_id=disciplina.id).first()
                        if nota:
                            nota.valor = valor_float
                        else:
                            nova_nota = Nota(valor=valor_float, aluno_id=aluno.id, disciplina_id=disciplina.id)
                            db.session.add(nova_nota)
            db.session.commit()
            flash('Notas salvas com sucesso!', 'success')
            return redirect(url_for('inserir_notas.inserir_notas'))

    return render_template('inserir_notas.html', turmas=turmas)

