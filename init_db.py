from app import app
from models import db

with app.app_context():
    db.create_all()
    print("funfou as tabelas mrm")

#banco ja criado, não precisa rodar novamente este código