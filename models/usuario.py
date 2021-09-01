from db import db
from sqlalchemy.orm import backref
from typing import List
from models.contato import ContatoModel


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.BigInteger, nullable=False, unique=True)
    contatos = db.relationship('ContatoModel', lazy='joined', backref="usuarios")

    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento

    def __repr__(self):
        return f'UsuarioModel(id={self.id}, nome={self.nome}, documento={self.documento}, contatos={self.contatos})'

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'documento': self.documento, 'contatos': self.contatos}

    @classmethod
    def find_by_documento(cls, documento) -> "UsuarioModel":
        return cls.query.filter_by(documento=documento).first()

    @classmethod
    def find_by_id(cls, _id) -> "UsuarioModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UsuarioModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
