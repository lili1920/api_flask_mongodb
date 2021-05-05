from flask import Flask , jsonify,request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")#tiene que ser el mismo nombre que se definio en docker compose
										# aca el cliente esta conectado a la base de datos db

db = client.SentencesDatabase #SE CREA LA BASE DE DATOS


users = db["Users"] # SE CREA UNA COLECCION # 1 usuario peude tener + 1 frase - Hay que hacer uan coleccion de usuarios 
 					#y dentro de cada uno va un documento embebido y con su frase
class Register(Resource):
	def post(self):
		#obtener lo que posteo el usuario
		postedData =request.get_json()

		#obtener los datos del usuario
		username = postedData["username"]
		password = postedData["password"]

		passwd = b'password'
		hashed = bcrypt.hashpw(passwd.encode('utf8'),bcrypt.gensalt())

		user.insert({
			"username":username,
			"Password":hashed,
			"Sentence":"",
			"Tokens":6

			})

		retJson = {
			"status":200,
			"msg":"sign up ok"
		}
		return jsonify(retJson)

def verifyPw(username, password):
		hashed_pw = users.find({
		"Username":username

		}) [0]["Password"]

		if bcrypt.hashpw(passwd.encode('utf8'),hashed_pw)==hashed_pw:
			return True
		else:
			return False 

def countTokens(username):
		tokens = users.find({
			"Username":username

		})[0]["Tokens"]

		return tokens		

class Store(Resource):
	def post(self):
		#obtener lo que posteo el usuario
		postedData =request.get_json()

		#leer los datos
		username = postedData["username"]
		password = postedData["password"]
		sentence = postedData["sentence"]

		# verificar el usuario

		correct_pw = verifyPw(username, password)

		if not correct_pw:
			retJson = {
				"status":302
			}
			return jsonify(retJson)

		#verificar si tiene token
		num_tokens = countokens(username)
		if num_tokens<=0:
			retJson = {
				"status":301
			}
			return jsonify(retJson)


		#almacenar la informacion y retornar 200 			
		users.update({
			"Username":username
		},{
			"$set":{
			"Sentence":sentence,
			"Tokens":num_tokens-1
			}			
		})

		retJson = {
			"status":200,
			"msg":"saved info"
		}

		return jsonify(retJson)



api.add_resource(Register, '/register')		
api.add_resource(Store,'/Store')

if __name__ == '__main__':
	app.run(host='0.0.0.0')

	