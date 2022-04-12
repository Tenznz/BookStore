import json

from flask import Blueprint, request

from user import db
from .models import Cart, CartItem


carts = Blueprint("carts", __name__, url_prefix="/carts")


@carts.route("/add", methods=["POST"])
def add():
    try:
        request_data = json.loads(request.data)
        total_quantity = request_data.get("total_quantity")
        total_price = request_data.get("total_price")
        status = request_data.get("status")
        user_id = request_data.get("user_id")

        if status == 0:
            cart = db.session.query(Cart).filter_by(status=0).one()
        else:
            cart = Cart(total_quantity=total_quantity, total_price=total_price, status=status, user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        new_cart_item = CartItem(user_id=user_id, cart_id=cart.cart_id, book_id=request_data.get("book_id"))
        db.session.add(new_cart_item)
        db.session.commit()
        return {
            "message": "successfully"
        }
    except Exception as e:
        return {
            "error_message": str(e)
        }
