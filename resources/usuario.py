from flask import request
from flask_restplus import Resource, fields

from models.usuario import UsuarioModel
from models.contato import ContatoModel
from schemas.usuario import UsuarioSchema, UsuarioSaveSchema
from schemas.contato import ContatoSchema

from server.instance import server

usuario_ns = server.usuario_ns
contato_ns = server.contato_ns

ITEM_NOT_FOUND = "Usuario nao encontrado."


usuario_schema = UsuarioSchema()
usuarioSave_schema = UsuarioSaveSchema()
contato_schema = ContatoSchema()
usuario_list_schema = UsuarioSchema(many=True)
contato_list_schema = ContatoSchema(many=True)


itemContato = contato_ns.model('Contato', {
    'email': fields.String('email@email.com'),
    'principal': fields.Boolean(0),
    'id': fields.Integer(0),
    'telefone': fields.Integer(0),
    'usuario_id': fields.Integer(0)
})

# Model required by flask_restplus for expect
itemUsuario = usuario_ns.model('Usuario', {
    'nome': fields.String('Nome'),
    'documento': fields.Integer(0),
    'id': fields.Integer(0),
    'contatos': fields.Nested(ContatoSchema())
})



class Usuario(Resource):

   def get(self, documento):
        user_data = UsuarioModel.find_by_documento(documento)
        if user_data:
            return usuario_schema.dump(user_data)
        return {'message': ITEM_NOT_FOUND}, 404

   def delete(self, documento):
        user_data = UsuarioModel.find_by_documento(documento)
        if user_data:

           contatos = ContatoModel.find_all_by_usuario(user_data.id)
           for contato in contatos:
                contato.delete_from_db()

           user_data.delete_from_db()
           return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

   @usuario_ns.expect(itemUsuario)
   def put(self, documento):
        usuario_data = UsuarioModel.find_by_documento(documento)
        usuario_json = request.get_json()

        if usuario_data:
            usuario_data.nome = usuario_json['nome']
            usuario_data.documento = usuario_json['documento']
        else:
            usuario_data = UsuarioModel(usuario_json['nome'], usuario_json['documento'])

        usuario_data.save_to_db()

        for contato in usuario_data.contatos:
             contato.delete_from_db()

        for contato in usuario_json['contatos']:
             contato = ContatoModel(contato['email'], contato['telefone'], contato['principal'])
             contato.usuario_id = usuario_data.id
             contato.save_to_db()

        return usuario_schema.dump(usuario_data), 201

class Contato(Resource):
   
   @contato_ns.expect(itemContato)
   def put(self, documento):
        usuario_data = UsuarioModel.find_by_documento(documento)
        contatos_json = request.get_json()

        if usuario_data:
            for contato in usuario_data.contatos:
                contato.delete_from_db()

            for contato in contatos_json:
                contato = ContatoModel(contato['email'], contato['telefone'], contato['principal'])
                contato.usuario_id = usuario_data.id
                contato.save_to_db()
        else:
            return {'message': ITEM_NOT_FOUND}, 404

        usuario_data = UsuarioModel.find_by_documento(documento)

        return usuario_schema.dump(usuario_data), 201


class UsuarioList(Resource):
     @usuario_ns.doc('Buscar todos')
     def get(self):
         return usuario_list_schema.dump(UsuarioModel.find_all()), 200

   
     @usuario_ns.doc('Criar usuario')
     def post(self):
         usuario_json = request.get_json()

         usuario_data = UsuarioModel(usuario_json['nome'], usuario_json['documento'])
         usuario_data.save_to_db()

         for contato in usuario_json['contatos']:
             contato = ContatoModel(contato['email'], contato['telefone'], contato['principal'])
             contato.usuario_id = usuario_data.id
             contato.save_to_db()

         return usuario_schema.dump(usuario_data), 201
