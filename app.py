from flask_mail import Mail

from books.routes import book
from user import app


mail = Mail(app)
if __name__ == "__main__":
    from user.routes import user
    app.register_blueprint(user)
    app.register_blueprint(book)
    app.run(debug=True)

