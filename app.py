from flask import Flask, render_template, request, jsonify
from flask_api import status
import configparser
import psycopg2
 


app = Flask(__name__)
config = configparser.ConfigParser()
config.read('padronapi.ini')
cnx=psycopg2.connect(dbname=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'], host=config['DB']['host'], port=config['DB']['port'])
cur=cnx.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/api/v1/provincias',methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincias():
    if request.method == 'GET':
        cur.execute("SELECT * FROM provincia;")
        dataJson = []
        for provincia in cur.fetchall():
            dataDict = {
                'codigo': provincia[0],
                'nombre': provincia[1]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para provincias'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

@app.route('/api/v1/cantones',methods=['POST', 'GET', 'DELETE', 'PUT'])
def cantones():
    if request.method == 'GET':
        cur.execute("SELECT provincia.nombre, canton.codigo, canton.nombre FROM canton, provincia WHERE canton.provincia = provincia.codigo;")
        dataJson = []
        for canton in cur.fetchall():
            dataDict = {
                'Provincia': canton[0],
                'codigo': canton[1],
                'nombre': canton[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para provincias'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED





@app.route('/api/v1/provincia/<string:codigo>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincia(codigo):
    if request.method == 'GET':
        cur.execute("SELECT * FROM provincia WHERE codigo=%s;",(codigo,))
        provincia=cur.fetchone()
        if provincia is None :
            content = {'Error de código': 'La provincia con el código {} no existe.'.format(codigo)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'codigo': provincia[0],
                'nombre': provincia[1]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/canton/<string:codigo>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def canton(codigo):
    if request.method == 'GET':
        cur.execute("SELECT provincia.nombre, canton.codigo, canton.nombre FROM canton, provincia WHERE canton.provincia = provincia.codigo AND canton.codigo=%s;",(codigo,))
        canton=cur.fetchall()
        if canton is None :
            content = {'Error de código': 'La canton con el código {} no existe.'.format(codigo)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'provincia': canton[0],
		'codigo': canton[1],
                'nombre': canton[2]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/cuidadanos/<string:pagina>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def cuidadano(pagina):
    page=int(pagina)*500
    if request.method == 'GET':
        cur.execute("select * from ciudadano LIMIT '500' OFFSET %s;",(str(page),))
        dataJson = []
        for cuidadano in cur.fetchall():
            if cuidadano is None :
             content = {'Error de código': 'La pagina con el código {} no existe.'.format(codigo)}
             return content, status.HTTP_404_NOT_FOUND
            else :
             dataDict = {
             'cedula': cuidadano[0],
             'vencimiento': cuidadano[1],
             'sexo': cuidadano[2],
             'nombre': cuidadano[3],
             'apellido1': cuidadano[4],
             'apellido2': cuidadano[5],
             'provincia': cuidadano[6],
             'canton': cuidadano[7],
             'distrito': cuidadano[8],
             'junta': str(cuidadano[9]),
             }
             dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK

    else :
        content = {'Error de método': 'Sólo se soporta GET para provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED



@app.route('/api/v1/cuidadano/<string:codigo>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def cuidadanoid(codigo):
    if request.method == 'GET':
        cur.execute("select * from ciudadano where cedula=%s;",(codigo,))
        cuidadano=cur.fetchone()
        if cuidadano is None :
            content = {'Error de código': 'el ciudadano con el código {} no existe.'.format(codigo)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
            'cedula': cuidadano[0],
             'vencimiento': cuidadano[1],
             'sexo': cuidadano[2],
             'nombre': cuidadano[3],
             'apellido1': cuidadano[4],
             'apellido2': cuidadano[5],
             'provincia': cuidadano[6],
             'canton': cuidadano[7],
             'distrito': cuidadano[8],
             'junta': str(cuidadano[9]),
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED







@app.route('/api/v1/distrito/<string:codigo>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def distrito(codigo):
    if request.method == 'GET':
        cur.execute("SELECT provincia.nombre, distrito.canton, distrito.codigo, distrito.nombre FROM distrito, provincia WHERE distrito.provincia = provincia.codigo AND distrito.codigo=%s;",(codigo,))
        distrito=cur.fetchall()
        if distrito is None :
            content = {'Error de código': 'La distrito con el código {} no existe.'.format(codigo)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'provincia': distrito[0],
				'Canton': distrito[1],
				'Codigo': distrito[2],
                'nombre': distrito[3]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para distrito'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED



@app.route('/api/v1/distritos',methods=['POST', 'GET', 'DELETE', 'PUT'])
def distritos():
    if request.method == 'GET':
        cur.execute("SELECT provincia.nombre, distrito.canton, distrito.codigo, distrito.nombre FROM distrito, provincia WHERE distrito.provincia = provincia.codigo;")
        dataJson = []
        for distrito in cur.fetchall():
            dataDict = {
           'provincia': distrito[0],
                                'Canton': distrito[1],
                                'Codigo': distrito[2],
                'nombre': distrito[3]

            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Sólo se soporta GET para provincias'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED




if __name__ == '__main__':
    app.debug = True
    app.run()

