from flask import Blueprint, render_template, request, send_file, make_response
from flask_login import login_required
from models import db, Turma, Aluno, Disciplina, Nota
from weasyprint import HTML
from datetime import datetime
from io import BytesIO

gerar_relatorio_bp = Blueprint('gerar_relatorio', __name__)

@gerar_relatorio_bp.route('/gerar_relatorio', methods=['GET', 'POST'])
@login_required
def gerar_relatorio():
    if request.method == 'POST':
        matricula_aluno = request.form.get('matricula_aluno')

        aluno = db.session.query(Aluno).filter_by(matricula=matricula_aluno).first()

        if not aluno:
            mensagem = "Matricula não encontrada"
            return render_template('400.html', mensagem = mensagem)

        disciplinas = aluno.turma.disciplinas if aluno.turma else []

        notas = {
            nota.disciplina_id: nota.valor
            for nota in db.session.query(Nota).filter_by(aluno_id=aluno.id).all()
        }

        valores = [valor for valor in notas.values() if valor is not None]
        media = sum(valores) / len(valores) if valores else None

        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        html = render_template(
            "boletim_aluno.html",
            aluno=aluno,
            disciplinas=disciplinas,
            notas=notas,
            media=media,
            timestamp=timestamp
        )

        pdf = HTML(string=html, base_url=request.root_url).write_pdf()

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=boletim_{aluno.nome}.pdf'

        return response

    return render_template('gerar_relatorio.html')
