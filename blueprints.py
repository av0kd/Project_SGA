from routes import (
    adicionar_alunos_bp, alunos_adicionados_bp, pesquisar_alunos_bp,
    aluno_pesquisado_bp, editar_alunos_bp, aluno_editado_bp,
    deletar_aluno_bp, aluno_deletado_bp, criar_turmas_bp, turmas_criadas_bp, pesquisar_turmas_bp,
    turmas_pesquisadas_bp, deletar_turmas_bp, turmas_deletadas_bp,
    cadastrar_disciplinas_bp, disciplina_cadastrada_bp, consultar_disciplina_bp,
    disciplina_consultada_bp, vincular_disciplina_bp, disciplina_vinculada_bp,
    inserir_notas_bp, gerar_relatorio_bp, register_user_bp, index_bp, logout_user_bp
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

    vincular = [
        vincular_disciplina_bp, disciplina_vinculada_bp
    ]

    inserir_notas = [
        inserir_notas_bp
    ]
    
    gerar_relatorio = [
        gerar_relatorio_bp
    ]

    login_register = [ 
        register_user_bp, index_bp, logout_user_bp
    ]

    for bp in alunos + turmas + disciplinas + vincular + inserir_notas + gerar_relatorio + login_register:
        app.register_blueprint(bp)
