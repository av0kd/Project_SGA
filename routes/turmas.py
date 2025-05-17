from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

criar_turmas_bp = Blueprint('criar_turmas', __name__)
turmas_criadas_bp = Blueprint('turmas_criadas', __name__)
pesquisar_turmas_bp = Blueprint('pesquisar_turmas', __name__)
turmas_pesquisadas_bp = Blueprint('turmas_pesquisadas', __name__)
deletar_turmas_bp = Blueprint('deletar_turmas', __name__)
turmas_deletadas_bp = Blueprint('turmas_deletadas', __name__)
editar_turmas_bp = Blueprint('editar_turmas', __name__)
turma_editada_bp = Blueprint('turma_editada', __name__)

@criar_turmas_bp.route('/criar_turmas')
@login_required
def criar_turmas():
    disciplinas = Disciplina.query.all()
    return render_template('criar_turmas.html', disciplinas=disciplinas)


@turmas_criadas_bp.route('/turmas_criadas', methods=['POST'])
@login_required
def turmas_criadas():
    nome_turma = request.form.get('nome_turma')
    serie_turma = request.form.get('serie_turma')
    disciplinas_selecionadas = request.form.getlist('disciplinas_turma')

    if not nome_turma or not serie_turma or not disciplinas_selecionadas:
        return render_template('400.html')

    turma_existente = Turma.query.filter_by(nome=nome_turma, serie=serie_turma).first()
    if turma_existente:
        return f"{turma_existente} já existe uma turma com esse nome"


    nova_turma = Turma(nome=nome_turma, serie=serie_turma)

    for disciplina_id in disciplinas_selecionadas:
        disciplina = Disciplina.query.get(disciplina_id)
        if disciplina:
            nova_turma.disciplinas.append(disciplina)

    db.session.add(nova_turma)
    db.session.commit()

    return render_template('turmas_criadas.html', turma=nova_turma)


@pesquisar_turmas_bp.route('/pesquisar_turmas')
@login_required
def pesquisar_turmas():
    return render_template('pesquisar_turmas.html')

@turmas_pesquisadas_bp.route('/turmas_pesquisadas', methods=['POST'])
@login_required
def turmas_pesquisadas():
    nome_turma = request.form.get('nome_turma', '').strip()
    serie_turma = request.form.get('serie_turma', '').strip()

    query = Turma.query

    if nome_turma:
        query = query.filter(Turma.nome.ilike(f"%{nome_turma}%"))
    if serie_turma:
        query = query.filter(Turma.serie.ilike(f"%{serie_turma}%"))

    turmas_filtradas = query.all()

    if not turmas_filtradas:
        return render_template('400.html', mensagem="Nenhuma turma encontrada.")

    return render_template('turmas_pesquisadas.html', turmas=turmas_filtradas)

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@deletar_turmas_bp.route('/deletar_turma')
@login_required
def deletar_turma():
    turmas = Turma.query.all()
    return render_template('deletar_turma.html', turmas=turmas)

@turmas_deletadas_bp.route('/turma_deletada', methods=['POST'])
@login_required
def turma_deletada():
    turma_id = request.form.get("turma_id")

    if not turma_id:
        return render_template('400.html')

    turma = Turma.query.get(turma_id)

    if not turma:
        return render_template('400.html')

    # Desvincula os alunos da turma
    for aluno in turma.alunos:
        aluno.turma_id = None
        aluno.serie = None  # Opcional: também limpar a série se desejar

    # Agora pode deletar a turma
    db.session.delete(turma)
    db.session.commit()

    return render_template('turma_deletada.html')

@editar_turmas_bp.route('/editar_turmas', methods=['GET'])
@login_required
def editar_turma():
    turmas = Turma.query.all()
    turma_id = request.args.get('turma_id')
    turma_selecionada = Turma.query.get(turma_id) if turma_id else None
    disciplinas = Disciplina.query.all()

    return render_template(
        'editar_turmas.html',
        turmas=turmas,
        turma_selecionada=turma_selecionada,
        disciplinas=disciplinas
    )

@turma_editada_bp.route('/turma_editada', methods=['POST'])
@login_required
def turma_editada():
    turma_id = request.form.get('turma_id')
    nova_nome = request.form.get('nome')
    nova_serie = request.form.get('serie')
    disciplinas_selecionadas = request.form.getlist('disciplinas')

    turma = Turma.query.get(turma_id)
    if not turma:
        return render_template('400.html', mensagem="Turma não encontrada.")

    if nova_nome:
        turma.nome = nova_nome
    if nova_serie:
        turma.serie = nova_serie

    turma.disciplinas.clear()
    for disc_id in disciplinas_selecionadas:
        disc = Disciplina.query.get(disc_id)
        if disc:
            turma.disciplinas.append(disc)

    db.session.commit()

    return render_template('turma_editada.html', turma=turma)
