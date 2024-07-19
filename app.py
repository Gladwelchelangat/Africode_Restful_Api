from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
app.app_context().push()
db.create_all()


user_args=reqparse.RequestParser()
user_args.add_argument('username', type=str, help='Username is required', required=True)
user_args.add_argument('email', type=str, help='email is required', required=True)

userFields= {"id":fields.Integer,"username":fields.String,"email":fields.String}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    

class User(Resource):
    @marshal_with(userFields)
    def get (self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user
    @marshal_with(userFields)
    def patch(self,id):
        args=user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        user.username = args['username'] 
        user.email = args['email'] 
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users=UserModel.query.all()
        return users
    
api.add_resource(User,'/api/users/<int:id>')
api.add_resource(Users,"/api/users/")

@app.route('/')
def home():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True)
 