from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
import os


if  'MONGODB_HOST' in os.environ:
    MONGODB_HOST = os.environ["MONGODB_HOST"]
else : 
    MONGODB_HOST = '0.0.0.0'
    
if "MONGODB_PORT" in os.environ:
    MONGODB_PORT = os.environ["MONGODB_PORT"]
else :
    MONGODB_PORT = '27017'

if  "MONGODB_DB"  in os.environ:
    MONGODB_DB = os.environ["MONGODB_DB"]
else :
    MONGODB_DB = 'registro'

if "MONGODB_COLECCTION"  in os.environ:
    MONGODB_COLECCTION = os.environ["MONGODB_COLECCTION"]
else :
    MONGODB_COLECCTION = 'docker2'

if "FLASK_HOST"   in os.environ:
    FLASK_HOST = os.environ["FLASK_HOST"]
else :
    FLASK_HOST =  '0.0.0.0'


if "FLASK_PORT"   in os.environ:
    FLASK_PORT = os.environ["FLASK_PORT"]
else :
    FLASK_PORT = 5000


#MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
#MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_PASSWORD"]





#MONGO_INITDB_ROOT_USERNAME='mongoadmin'
#MONGO_INITDB_ROOT_PASSWORD='secret'

URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT +  "/"

app = Flask(__name__)


class MongoAPI:
    def __init__(self, data=None):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        ''' 
        self.cliente = MongoClient(URI_CONNECTION, username = MONGO_INITDB_ROOT_USERNAME ,
                                password= MONGO_INITDB_ROOT_PASSWORD, 
                                serverSelectionTimeoutMS=MONGODB_TIMEOUT,maxPoolSize=10)                                                            # Docker and we are using Docker Compose
        '''
        
        self.cliente = MongoClient(URI_CONNECTION)
        
        base = 'IshmeetDB'
        coleccion = 'people'
        
        cursor = self.cliente[MONGODB_DB]
        self.coleccion = cursor[MONGODB_COLECCTION]
        self.data = data

    def read(self):
        log.info('<<GET>> Leyendo todos los elementos')
        documents = self.coleccion.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, datos):
        log.info('Escribiendo Datos en Mongo')
        nuevo_documento = datos
        response = self.coleccion.insert_one(nuevo_documento)
        output = {'Estatus': 'Insertado correctamente',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self, data):
        log.info('Actualizando datos')
        filt = data['Filtro']
        updated_data = {"$set": data['Datos']}
        response = self.coleccion.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Eliminando datos')
        filt = data['Filtro']
        response = self.coleccion.delete_one(filt)
        output = {'Status': 'Eliminado correctamente' if response.deleted_count > 0 else "Document not found."}
        return output



@app.route('/registro', methods=['GET'])
def mongo_read():
    #data = request.json
    
    obj1 = MongoAPI()
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/registro', methods=['POST'])
def mongo_write():
    datos = request.json
    if datos is None or datos == {} :
        return Response(response=json.dumps({"Error": "No se  han enviado dtos"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI()
    response = obj1.write(datos)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/registro', methods=['PUT'])
def mongo_update():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data or 'Datos' not in data:
        return Response(response=json.dumps({"Error": "Introdusca el filtro o los datos "}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI()
    response = obj1.update(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/registro', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data:
        return Response(response=json.dumps({"Error": "Introdusca el filtro"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI()
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route("/", methods=["GET"])
def get_ips():
    #print(request.environ)
    return Response(response=json.dumps({'IP Remota': request.remote_addr, 'IP Host':request.environ['SERVER_NAME']}),
                    status=200,
                    mimetype='application/json')
    #return jsonify({'IP Remota': request.remote_addr, 'IP Host':request.environ['SERVER_NAME']  }), 200

if __name__ == '__main__':
    app.run(debug=True, port=FLASK_PORT, host=FLASK_HOST)


