from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina

gerar_relatorio_bp = Blueprint('gerar_relatorio', __name__)

@gerar_relatorio_bp.route('/gerar_relatorio', methods=['GET', 'POST'])
@login_required
def gerar_relatorio():
    if request.method == 'POST':
        matricula_aluno = request.form.get('matricula_aluno')

        # Buscando o aluno pela matrícula
        resultado = db.session.query(
            Aluno.nome, Turma.nome, Disciplina.nome, Nota.valor
        ).join(Turma, Aluno.turma_id == Turma.id) \
         .join(Nota, Nota.aluno_id == Aluno.id) \
         .join(Disciplina, Nota.disciplina_id == Disciplina.id) \
         .filter(Aluno.matricula == matricula_aluno).all()

        if not resultado:
            return "Aluno não encontrado ou sem notas cadastradas."

        nome_aluno = resultado[0][0]
        nome_turma = resultado[0][1]
        notas_disciplinas = [(disciplina, nota) for _, _, disciplina, nota in resultado]

        notas = [nota for _, nota in notas_disciplinas]
        media = sum(notas) / len(notas)

        nome_arquivo = f"relatorio_notas_{nome_aluno}.txt"

        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write("SGA BOLETIM\n")
            arquivo.write(f"\nNome do Aluno: {nome_aluno}\n")
            arquivo.write(f"Turma: {nome_turma}\n\n")
            arquivo.write("Disciplina\tNota\n")
            for disciplina, nota in notas_disciplinas:
                arquivo.write(f"{disciplina}\t{nota}\n")
                
            arquivo.write(f"\nMédia Final: {media:.2f}\n")

        return send_file(nome_arquivo, as_attachment=True)

    # Para o caso de o método ser GET ou se o usuário acessar diretamente a página
    return render_template('gerar_relatorio.html')