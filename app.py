from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from models import db, Turma, Aluno, Disciplina, Nota, AlunoDisciplina
from blueprints import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

register_blueprints(app)

@app.route('/')
def inicio():
    return render_template('index.html')


#<------------------AQUI ENCERRA A PARTE DO CREATE E RECOVERY DAS TURMAS------------------>

#Rotas para disciplinas

@app.route('/vincular_disciplina', methods=['POST', 'GET'])
def vincular_disciplina():
    return render_template('vincular_disciplina.html')

@app.route('/disciplina_vinculada', methods=["POST"])
def disciplina_vinculada():
    matricula_aluno = request.form.get('matricula_aluno')
    disciplina_id = request.form.get('disciplina_id')

    # Buscar o aluno pela matricula e disciplina pelo ID
    aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()
    disciplina = Disciplina.query.get(disciplina_id)

    if not aluno:
        return "Aluno não encontrado", 400
    if not disciplina:
        return "Disciplina não encontrada", 400

    # Verifica se o aluno já está vinculado à disciplina
    if AlunoDisciplina.query.filter_by(aluno_id=aluno.id, disciplina_id=disciplina.id).first():
        return "O aluno já está vinculado a essa disciplina!", 400

    # Criar o vínculo entre aluno e disciplina
    novo_vinculo = AlunoDisciplina(aluno_id=aluno.id, disciplina_id=disciplina.id)
    db.session.add(novo_vinculo)
    db.session.commit()

    return "Aluno vinculado à disciplina com sucesso!"

#<------------------AQUI ENCERRA A PARTE DE CRIAR/CONSULTAR/VINCULAR AS DISCIPLINAS------------------>

@app.route('/inserir_notas', methods=['GET', 'POST'])
def inserir_notas():
    if request.method == 'POST':
        matricula_aluno = request.form.get('matricula_aluno')
        
        # Buscar o aluno pela matrícula
        aluno = Aluno.query.filter_by(matricula=matricula_aluno).first()

        if not aluno:
            return "Aluno não encontrado", 404

        # Se houver notas no formulário, salvar no banco de dados
        notas_enviadas = {key: value for key, value in request.form.items() if key.startswith('nota_')}
        
        if notas_enviadas:
            for key, valor_nota in notas_enviadas.items():
                disciplina_id = int(key.split('_')[1])  # Extrai o ID da disciplina
                valor_nota = float(valor_nota)

                # Verifica se a nota já existe
                nota_existente = Nota.query.filter_by(aluno_id=aluno.id, disciplina_id=disciplina_id).first()

                if nota_existente:
                    nota_existente.valor = valor_nota  # Atualiza a nota existente
                else:
                    nova_nota = Nota(aluno_id=aluno.id, disciplina_id=disciplina_id, valor=valor_nota)
                    db.session.add(nova_nota)  # Insere uma nova nota

            db.session.commit()

        # Renderizar o formulário com as disciplinas do aluno
        return render_template('inserir_notas.html', aluno=aluno)

    return render_template('inserir_notas.html', aluno=None)


@app.route('/gerar_relatorio', methods=['GET', 'POST'])
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

#<------------------AQUI ENCERRA A PARTE DE VINCULAR AS NOTAS E GERAR UM TXT DAS NOTAS------------------>

if __name__ == '__main__':
    app.run(debug=True)