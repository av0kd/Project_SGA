from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    nome = db.Column(db.String(100), nullable=False)
    notas = db.relationship('Nota', backref='disciplina', lazy=True)  # Relacionamento com Nota

    def __repr__(self):
        return f'<Disciplina {self.nome}>'

# Tabela de Notas
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)  # Chave estrangeira para Aluno
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)  # Chave estrangeira para Disciplina

    def __repr__(self):
        return f'<Nota {self.valor}>'
