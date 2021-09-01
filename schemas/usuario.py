from flask_sqlalchemy import model
from schemas.contato import ContatoSchema
from ma import ma

from models.usuario import UsuarioModel

from marshmallow import Schema, fields


class UsuarioSchema(Schema):
    load_instance = True
    id = fields.Integer()
    nome = fields.String()
    documento = fields.Integer()
    contatos =  fields.List(fields.Nested(ContatoSchema))
  

class UsuarioSaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True




     
