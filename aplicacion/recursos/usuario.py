from flask_restful import Resource, reqparse
from aplicacion.modelos.usuario import UsuarioModel

class Usuario(Resource):

    def get(self, _id):
        usuario = UsuarioModel.buscar_por_id(_id)

        if usuario:
            return usuario.obtener_datos()
        
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404
    
    def delete(self, _id):
        usuario = UsuarioModel.buscar_por_id(_id)
        
        if usuario:
            try:
                usuario.eliminar()
                return {'message': 'Usuario eliminado con éxito'}, 200
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación'}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404
        
class Usuarios(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int,
        required=False,
        help="Debe ingresar un ID de usuario"
    )
    parser.add_argument('username',
        type=str,
        required=True,
        help="Debe ingresar un nombre de usuario"
    )
    parser.add_argument('salt',
        type=str,
        required=False,
        help="Debe ingresar un salt para el usuario."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Debe ingresar un password para el usuario."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )

    def get(self):
        return {'usuarios': list(map(lambda x: x.obtener_datos(), UsuarioModel.query.filter_by(activo=1)))}

    def post(self):
        data = Usuarios.parser.parse_args()

        if UsuarioModel.buscar_username(data['username']):
            return {'message': "Ya existe un usuario llamado '{}'.".format(data['username'])}, 400

        usuario = UsuarioModel(data['username'], data['password'])
        usuario.activo = data['activo'] if data['activo'] else 0

        try:
            usuario.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
       
        return usuario.obtener_datos(), 201
    
    def put(self):
        data = Usuarios.parser.parse_args()

        if data['id'] == None:
            usuario = UsuarioModel(data['username'], data['password'])
            usuario.salt = usuario.salt if data['salt'] == None else data['salt']
            usuario.activo = usuario.activo if data['activo'] == None else data['activo']

            try:
                usuario.guardar()
            except:
                return {"message": "No se pudo resolver su petición."}, 500  
            
            return usuario.obtener_datos(), 201

        else:
            code = 200
            usuario = UsuarioModel.buscar_por_id(data['id'])
        
            if usuario:
                usuario.username = data['username']
                usuario.password = data['password']
            else:
                usuario = UsuarioModel(data['username'], data['password'])
                code = 201

            usuario.salt = usuario.salt if data['salt'] == None else data['salt']
            usuario.activo = usuario.activo if data['activo'] == None else data['activo']

            try:
                usuario.guardar()
            except:
                return {"message": "No se pudo resolver su petición."}, 500
            
            return usuario.obtener_datos(), code
    