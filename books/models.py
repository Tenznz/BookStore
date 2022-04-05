from user import db


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, book_name, author, price, user_id):
        self.book_name = book_name
        self.author = author
        self.price = price
        self.user_id = user_id

    def __str__(self):
        return {"book_name": self.book_name, "author": self.author, "price": self.price}
