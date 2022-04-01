from books.routes import book
from user import app
from user.routes import user


if __name__ == "__main__":
    app.register_blueprint(user)
    app.register_blueprint(book)
    app.run(debug=True)
