import json
import logging

from flask import request, jsonify, Blueprint

from user import db
from books.models import Books

book = Blueprint("book", __name__, url_prefix="/books")


@book.route('/add', methods=["POST"])
def create():
    """
    bookstore curd operation
    :return: message successful or not
    """
    try:
        if request.method == "POST":
            book_info = json.loads(request.data)
            book_name = book_info.get("book_name")
            author = book_info.get("author")
            price = book_info.get("price")
            user_id = book_info.get("user_id")

            newbook = Books(book_name=book_name, author=author, price=price, user_id=user_id)
            db.session.add(newbook)
            db.session.commit()
            return jsonify({
                "message": "new book is created",
                "data": newbook.__str__()
            })
    except Exception as e:
        logging.error(e)
        return jsonify({'message': "error"})


@book.route("/<int:user_id>", methods=["GET"])
def get(user_id):
    """
    this method display all the books of specify user_id
    :param user_id:
    :return: list of books info
    """
    try:
        if request.method == "GET":
            books = Books.query.filter_by(user_id=user_id)
            return jsonify({
                'Books': list(x.__str__() for x in books)
            })
    except Exception as e:
        logging.error(e)
        return jsonify({'message': "error"})


@book.route("/put", methods=["PUT"])
def put():
    """
    this method is to update book details if found
    :return:update info
    """
    try:
        if request.method == "PUT":
            data = request.get_json()
            book_name = data.get('book_name')
            book = Books.query.filter_by(book_name=book_name).first()
            if not book:
                return jsonify({
                    "message": "Book name not found"
                })
            book.price = data.get("price")
            book.user_id = data.get("user_id")
            book.author = data.get("author")
            db.session.add(book)
            db.session.commit()
            return jsonify({
                "data": book.__str__()
            })
    except Exception as e:
        logging.error(e)
        return jsonify({
            "message": "error"
        })


@book.route("/delete", methods=['DELETE'])
def book_delete():
    """
    this method is to delete book from books data
    :return:message is deleted
    """
    try:
        data = json.loads(request.data)
        book_name = data.get('book_name')
        book = Books.query.filter_by(book_name=book_name).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({
                'message': 'book deleted'
            })
        else:
            return jsonify({
                'message': 'book not found'
            })
    except Exception as e:
        logging.error(e)
        return jsonify({
            "message": "error"
        })
