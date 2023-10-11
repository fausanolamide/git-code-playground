from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///somto.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student(name = {self.name}, gender = {self.gender})"

    def serialize(self):
        user = {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "phone": self.phone
        }
        return json.dumps(user)


user_post_args = reqparse.RequestParser()
user_post_args.add_argument(
    "name", type=str, help="name is required")
user_post_args.add_argument(
    "gender", type=str, help="gender is required")
user_post_args.add_argument("age", type=int, help="age needs to specified")
user_post_args.add_argument(
    "phone", type=int, help="phone of user is required")

resource_fields = {
    # 'id': fields.Integer,
    'name': fields.String,
    'gender': fields.String,
    'age': fields.Integer,
    'phone': fields.Integer
}


class Homepage(Resource):
    def get(self):
        return {"users": "account"}


class UsersResources(Resource):

    @marshal_with(resource_fields)
    def get(self):
        result = User.query.all()
        # if not result:
        #     return []
        return result

    def post(self):
        data = user_post_args.parse_args()
        name = data['name']
        gender = data['gender']
        age = data['age']
        phone = data['phone']
        user = User(
            name=name,
            gender=gender,
            age=age,
            phone=phone
        )
        db.session.add(user)
        db.session.commit()
        return user.serialize(), 201


api.add_resource(Homepage, "/")
api.add_resource(UsersResources, "/users")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
