from flask import request
from flask_restx import Resource, Namespace
from app.database import db
from app.models import Author, AuthorSchema

author_ns = Namespace('authors')

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

@author_ns.route('/')
class AuthorsView(Resource):
    def get(self):
        all_authors = db.session.query(Author).all()
        return authors_schema.dump(all_authors), 200


    def post(self):
        req_json = request.json
        new_author = Author(**req_json)

        with db.session.begin():
            db.session.add(new_author)

        return '', 201


@author_ns.route('/<int:aid>')
class AuthorView(Resource):
    def get(self, aid):
        author = db.session.query(Author).get(aid)
        return author_schema.dump(author), 200


    def put(self, aid):
        author = db.session.query(Author).get(id)
        req_json = request.json

        author.first_name = req_json.get('first_name')
        author.last_name = req_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204


    def patch(self, aid):
        author = db.session.query(Author).get(aid)
        req_json = request.json

        if "first_name" in req_json:
            author.first_name = req_json.get('first_name')
        if "last_name" in req_json:
            author.last_name = req_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204


    def delete(self, aid):
        author = db.session.query(Author).get(aid)

        db.session.delete(author)
        db.session.commit()

        return '', 204