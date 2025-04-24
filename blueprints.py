from routes import (
    adicionar_alunos_bp, alunos_adicionados_bp, pesquisar_alunos_bp,
    aluno_pesquisado_bp, editar_alunos_bp, aluno_editado_bp,
    deletar_aluno_bp, aluno_deletado_bp, criar_turmas_bp, turmas_criadas_bp, pesquisar_turmas_bp,
    turmas_pesquisadas_bp, deletar_turmas_bp, turmas_deletadas_bp,
    cadastrar_disciplinas_bp, disciplina_cadastrada_bp, consultar_disciplina_bp,
    disciplina_consultada_bp
)

def register_blueprints(app):
    alunos = [
        adicionar_alunos_bp, alunos_adicionados_bp, pesquisar_alunos_bp,
        aluno_pesquisado_bp, editar_alunos_bp, aluno_editado_bp,
        deletar_aluno_bp, aluno_deletado_bp
    ]

    turmas = [
        criar_turmas_bp, turmas_criadas_bp, pesquisar_turmas_bp,
        turmas_pesquisadas_bp, deletar_turmas_bp, turmas_deletadas_bp
    ]

    disciplinas = [
        cadastrar_disciplinas_bp, disciplina_cadastrada_bp, consultar_disciplina_bp,
        disciplina_consultada_bp
        ]
        

    for bp in alunos + turmas + disciplinas:
        app.register_blueprint(bp)
