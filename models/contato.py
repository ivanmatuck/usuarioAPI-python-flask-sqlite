from enum import unique

from sqlalchemy.orm import backref
from db import db
from typing import List


class ContatoModel(db.Model):
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.BigInteger, nullable=False)
    principal = db.Column(db.Boolean, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __init__(self, email, telefone, principal):
        self.email = email
        self.telefone = telefone
        self.principal = principal

    def __repr__(self):
        return f'ContatoModel(email={self.email}, telefone={self.telefone}, principal={self.principal})'

    def json(self):
        return {'email': self.email, 'telefone': self.telefone, 'principal' : self.principal}
  
    @classmethod
    def find_by_id(cls, _id) -> "ContatoModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ContatoModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_usuario(cls, usuario_id) -> List["ContatoModel"]:
        print(usuario_id)
        return cls.query.filter_by(usuario_id=usuario_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
