import json

from flask import Blueprint, request

from books.models import Books
from user import db
from .models import Cart, CartItem

carts = Blueprint("carts", __name__, url_prefix="/carts")


@carts.route("/addcart", methods=["POST"])
def add_cart():
    """
    get request userid and booklist and
    add to cart and cart item in database
    :return: cart_id, message
    """
    try:
        request_data = json.loads(request.data)
        book_list = request_data.get("book_list")
        user_id = request_data.get("user_id")
        total_price = 0
        total_quantity = sum(book_list.values())
        for book_id, quantity in book_list.items():
            books = db.session.query(Books).filter_by(book_id=book_id).one()
            total_price += books.price * quantity
        cur_cart = db.session.query(Cart).filter_by(user_id=user_id, status=0).first()
        # 0-active 1-inactive
        if not cur_cart:
            cur_cart = Cart(total_quantity=total_quantity, total_price=total_price, status=0, user_id=user_id)
            db.session.add(cur_cart)
            db.session.commit()
        else:
            cur_cart.total_price = cur_cart.total_price + total_price
        for book in book_list:
            cart_item = CartItem(user_id=user_id, cart_id=cur_cart.cart_id, book_id=book)
            db.session.add(cart_item)
            db.session.commit()
        return {
            "cart_id": cur_cart.cart_id,
            "message": "cart added successfully"
        }

    except Exception as e:
        return {
            "error_message": str(e)
        }


@carts.route("/getcart", methods=["GET"])
def get_cart():
    """
    get all the cart item by cart_id
    :return: cart_list
    """
    request_data = json.loads(request.data)
    cart_id = request_data.get("cart_id")
    cart_data = db.session.query(CartItem, Cart, Books) \
        .outerjoin(Cart, CartItem.cart_id == Cart.cart_id) \
        .filter_by(cart_id=cart_id) \
        .outerjoin(Books, CartItem.book_id == Books.book_id) \
        .all()
    if len(cart_data) == 0:
        return {
            "message": "no cart found"
        }
    cart_list = []
    for cart in cart_data:
        cart_list.append({
            "bookname": cart[2].book_name,
            "price": cart[2].price,
        })
    return {
        "cart_id": cart_id,
        "cart_data": cart_list
    }


@carts.route("/deletecart", methods=["DELETE"])
def delete_cart():
    """
    delete cart with cart items
    :return: message
    """
    request_data = json.loads(request.data)
    cart_id = request_data.get("cart_id")
    CartItem.query.filter_by(cart_id=cart_id).delete()
    Cart.query.filter_by(cart_id=cart_id).delete()
    db.session.commit()
    return {
        "message": "delete successfully"
    }
