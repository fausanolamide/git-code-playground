from flask import Flask, request
import json
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student(FirstName = {self.first_name}, LastName = {self.last_name})"

    def serialize(self):
        student = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone": self.phone
        }
        return json.dumps(student)


student_post_args = reqparse.RequestParser()
student_post_args.add_argument(
    "first_name", type=str, help="first name is required")
student_post_args.add_argument(
    "last_name", type=str, help="last name required")
student_post_args.add_argument("gender", type=str, help="gender is required")
student_post_args.add_argument("phone", type=int, help="phone is required")


resource_fields = {
    # 'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'gender': fields.String,
    'phone': fields.Integer
}


class StudentResource(Resource):
    @marshal_with(resource_fields)
    def get(self, student_id):
        result = Student.query.filter_by(id=student_id).first()
        if not result:
            abort(404, message="Could not find student with that id")
        return result

    # @marshal_with(resource_fields)
    # def put(self, student_id):
    #     data = request.json
    #     if not data:
    #         abort(404, message="not data provided")
    #     student = Student.query.get(student_id)
    #     if not student:
    #         abort(404,  message="Student doesn't exist, cannot update")

    #     for key, value in data.items():
    #         setattr(student, key, value)

    #     db.session.add(student)
    #     db.session.commit()
    #     return student.serialize(), 20

    @marshal_with(resource_fields)
    def delete(self, student_id):
        student = Student.query.filter_by(id=student_id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return "student deleted"
        abort(404, message="Student not found")


class StudentsResource(Resource):

    @marshal_with(resource_fields)
    def get(self):
        result = Student.query.all()
        return result

    def post(self):
        data = student_post_args.parse_args()
        first_name = data['first_name']
        last_name = data['last_name']
        gender = data['gender']
        phone = data['phone']
        student = Student(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone
        )
        db.session.add(student)
        db.session.commit()
        return student.serialize(), 201


class HomePage(Resource):
    def get(self):
        return {"Api": "version:0.4.5"}


api.add_resource(StudentResource, "/student/<int:student_id>")
api.add_resource(StudentsResource, "/students")
api.add_resource(HomePage, '/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
