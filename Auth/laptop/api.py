# Laptop Service

from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import os
from passlib.apps import custom_app_context as pass_info
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
# Instantiate the app
import time
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'UOCIS322'
auth = HTTPBasicAuth()
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDRESS'],27017)
db = client.tododb

users = db.userdb
user_id = 0

class CloseOnlyCSV(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        close = ""
    for i in lists:
            name = lists['name']
            description = lists['description']
            cl_time = description[1]
            close = name+cl_time
    return close
class OpenOnlyCSV(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        opent = ""
    for i in lists:
            name = lists['name']
            description = lists['description']
            op_time = description[0]
            opent = name+op_time
    return opent
class AllCSV(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        total = ""
    for i in lists:
            name = lists['name']
            description = lists['description']
            op_time = description[0]
            cl_time = description[1]
            total = name+op_time+cl_time

class Open(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        op = {}

        for i in lists:
            name = lists['name']
            description = lists['description']
            o_time = description[0]
            op[name] = o_time
        
        return op

class Close(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        cl = {}

        for i in lists:
            name = lists['name']
            description = lists['description']
            cl_time = description[1]
            cl[name] = cl_time
        
        return cl
class ListAll(Resource):
    def get(self):
        token = request.headers.get('token')
        authorized = verify_auth_token(token)

        if not authorized:
            return "Enter wrong token or time has expired", 401
        if(request.args.get('top'):
            top = int(request.args.get('top')
            lists = []
            lists = db.tododb.find().limit(top+1)
        else:
            lists = db.tododb.find()
        data.sort('name')
        all_l = {}

        for i in lists:
            name = lists['name']
            description = lists['description']
            a_list = description
            all_l[name] = a_list
        
        return all_l
def hash_password(password):
    return pass_info.encrypt(password)

@auth.password_auth
def password_auth(username,password):
    db_users = users.find({"username":username})

    db_e = de_users[0]
    hashh = db_e["password"]
    if pass_info.verify(password,hashh):
        return db_e
    else:
        return False
def auth_token(token):
    secure_key= Serializer(app.config['SECRET_KEY'])
    if not token:
        return None
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return "Correct"
def create_auth(user_id,expiration=45):
    s = Serializer(app.config['SECRET_KEY'],expires_in=experation)
    token = s.dumps({'id':current_id})
    return {'token':token,'duration':expiration}

@app.route("/laptop/register/page")
def register_page():
    return flask.render_template("register.html")

@app.route("/laptop/register",methods=['POST'])
def register():
    global user_id
    names = users.distinct("username")
    username = request.form.get("username")
    password = request.form.get("password")

    hashh = hash_password(password)
    password = None
    user = {"_id":user_id, "username":username,"password":hashh}
    users.insert_one(user)
    resp = {"Location":user_id,"username":username,"password":hashh}
    user_id +=1
    return flask.jsonify(result=resp),201

@app.route("/laptop/token/page")
def token_html():
    return flask.render_template("token.html")
@app.route("/laptop/token",methods=['GET'])
@auth.login_required
def get_token():
    username = request.authorization.username
    db_user = users.find({"username":username})
    db_e = db_user[0]

    user_id = db_e["_id"]
    token_dur = create_auth(user_id)
    token = token_dur['token']
    duration = token_dur['duration']
    resp = {'token':token_str,'duration':duration}
    return flask.jsonify(result=resp)

#return {
           # 'Laptops': ['Mac OS', 'Dell', 
          #  'Windozzee',
	 #   'Yet another laptop!',
	#    'Yet yet another laptop!'
   #         ]
  #      }

# Create routes
# Another way, without decorators
api.add_resource(ListAll,'/ListAll')
api.add_resource(ListAll,'/ListAll/json')
api.add_resource(ListAll,'/ListAll/csv')


api.add_resource(OpenOnlyCSV,'/OpenOnlyCSV/csv')
api.add_resource(CloseOnlyCSV,'/CloseOnlyCSV/csv')
api.add_resource(AllCSV,'/AllCSV/csv')
# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
