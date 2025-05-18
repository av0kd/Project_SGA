from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_user = db.Column(db.String(40), unique=True, nullable=False)
    nome_user = db.Column(db.String(100), nullable=False)
    senha_user = db.Column(db.String(128), nullable=False)
    cargo = db.Column(db.String(40), nullable=False)

    def get_id(self):
        return str(self.id)

turma_disciplina = db.Table('turma_disciplina',
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True),
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    serie = db.Column(db.String(50), nullable=False)  # Ex: '6° ano'
    
    alunos = db.relationship('Aluno', backref='turma', lazy=True)
    disciplinas = db.relationship('Disciplina', secondary=turma_disciplina, backref='turmas', lazy='subquery')

    def __repr__(self):
        return f'<Turma {self.nome} - {self.serie}>'

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)
    serie = db.Column(db.String(50), nullable=True)

    notas = db.relationship('Nota', backref='aluno', lazy='joined')
    disciplinas = db.relationship('Disciplina', secondary='aluno_disciplina', back_populates='alunos')

    def __init__(self, nome, matricula, turma_id=None):
        self.nome = nome
        self.matricula = matricula
        self.turma_id = turma_id
        self.serie = None

        if turma_id:
            turma = Turma.query.get(turma_id)
            if turma:
                self.serie = turma.serie
                for disciplina in turma.disciplinas:
                    self.disciplinas.append(disciplina)

    def __repr__(self):
        return f'<Aluno {self.nome} - {self.serie}>'

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    notas = db.relationship('Nota', backref='disciplina', lazy=True, cascade='all, delete')
    alunos = db.relationship('Aluno', secondary='aluno_disciplina', back_populates='disciplinas')

    def __repr__(self):
        return f'<Disciplina {self.nome}>'

class AlunoDisciplina(db.Model):
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)

    def __repr__(self):
        return f'<Nota {self.valor}>'