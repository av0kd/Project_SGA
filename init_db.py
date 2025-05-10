from app import app
from models import db

with app.app_context():
    db.create_all()
    print("Banco Criado!!")

#banco ja criado, não precisa rodar novamente este código

#caso precise recriar o banco, acesse a pasta instance e exclua o arquivo .db