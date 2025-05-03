from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_user = db.Column(db.String(40), unique=True, nullable=False)
    senha_user = db.Column(db.String(128), nullable=False)
    cargo = db.Column(db.String(40), nullable=False)

# Tabela de Turmas
class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)  # Relacionamento com Aluno

    def __repr__(self):
        return f'<Turma {self.nome}>'

# Tabela de Alunos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)  # Chave estrangeira para Turma
    notas = db.relationship('Nota', backref='aluno', lazy=True)  # Relacionamento com Nota

    def __repr__(self):
        return f'<Aluno {self.nome}>'

# Tabela de Disciplinas
class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    notas = db.relationship('Nota', backref='disciplina', lazy=True)  # Relacionamento com Nota

    def __repr__(self):
        return f'<Disciplina {self.nome}>'

# Tabela de associação para vincular o aluno a uma disciplina sem precisar vincular uma nota antes
class AlunoDisciplina(db.Model):
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    aluno = db.relationship('Aluno', backref=db.backref('disciplinas', lazy=True))
    disciplina = db.relationship('Disciplina', backref=db.backref('alunos', lazy=True))

    def __repr__(self):
        return f'<AlunoDisciplina {self.aluno.nome} - {self.disciplina.nome}>'

# Tabela de Notas
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)  # Chave estrangeira para Aluno
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)  # Chave estrangeira para Disciplina

    def __repr__(self):
        return f'<Nota {self.valor}>'
