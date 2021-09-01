from ma import ma
from models.contato import ContatoModel


class ContatoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContatoModel
        load_instance = True
