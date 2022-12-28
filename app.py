import os
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
api = Api(app)
book_ns = api.namespace('books')
author_ns = api.namespace('authors')


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    year = fields.Int()


class AuthorSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()


book_schema = BookSchema()
books_schema = BookSchema(many=True)
b1 = Book(id=1, name='test1', year=2021)
b2 = Book(id=2, name='test2', year=2022)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
a1 = Author(id=1, first_name='test1', last_name='test1')
a2 = Author(id=2, first_name='test2', last_name='test2')

with app.app_context():
    db.drop_all()
    db.create_all()

    with db.session.begin():
        db.session.add_all([b1, b2])
        db.session.add_all([a1, a2])


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200


    def post(self):
        req_json = request.json
        new_book = Book(**req_json)
        with db.session.begin():
            db.session.add(new_book)
        return '', 201


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        try:
            book = db.session.query(Book).filter(Book.id == bid).one()
            return book_schema.dump(book), 200
        except Exception as e:
            return str(e), 404


    def put(self, bid):
        book = db.session.query(Book).get(bid)
        req_json = request.json
        book.name = req_json.get('name')
        book.year = req_json.get('year')
        db.session.add(book)
        db.session.commit()
        return '', 204


    def patch(self, bid):
        book = db.session.query(Book).get(bid)
        req_json = request.json
        if "name" in req_json:
            book.name = req_json.get("name")
        if "age" in req_json:
            book.age = req_json.get("age")

        db.session.add(book)
        db.session.commit()

        return "", 204


    def delete(self, bid):
        book = db.session.query(Book).get(bid)
        db.session.delete(book)
        db.session.commit()
        return "", 204


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
