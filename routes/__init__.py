from .index import index_bp
from .logout import logout_user_bp

from .alunos import adicionar_alunos_bp, alunos_adicionados_bp, pesquisar_alunos_bp 
from .alunos import aluno_pesquisado_bp, editar_alunos_bp, aluno_editado_bp, deletar_aluno_bp, aluno_deletado_bp

from .turmas import criar_turmas_bp, turmas_criadas_bp, pesquisar_turmas_bp, turmas_pesquisadas_bp
from .turmas import deletar_turmas_bp, turmas_deletadas_bp, editar_turmas_bp, turma_editada_bp

from .disciplina import cadastrar_disciplinas_bp, disciplina_cadastrada_bp, consultar_disciplina_bp
from .disciplina import disciplina_consultada_bp, deletar_disciplina_bp, disciplina_deletada_bp

from .vincular import vincular_disciplina_bp, disciplina_vinculada_bp

from .inserir_notas import inserir_notas_bp

from .gerar_notas import gerar_relatorio_bp         

from .register import register_user_bp