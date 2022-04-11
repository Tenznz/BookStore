import json
import logging

from flask import Blueprint, request
from user import db

from orders.models import Orders, OrderItems

logging.basicConfig(filename='orderroute.txt', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
order = Blueprint("order", __name__, url_prefix="/orders")


@order.route("/add", methods=["POST"])
def add_order():
    try:
        order_data = json.loads(request.data)
        user_id = order_data.get("user_id")
        total_price = order_data.get("total_price")
        book_dic = order_data.get("book_list")
        status = order_data.get("status")
        total_quantity = sum(book_dic.values())
        new_order = Orders(user_id=user_id, total_price=total_price, total_quantity=total_quantity, status=status)
        db.session.add(new_order)
        db.session.commit()
        for key, value in book_dic.items():
            new_order_item = OrderItems(book_id=key, user_id=user_id, quantity=value, order_id=new_order.order_id)
            db.session.add(new_order_item)
            db.session.commit()
        return {
                   "order_id": new_order.order_id,
                   "message": "order add successfully"
               }, 201
    except Exception as e:
        print(e)
        logging.error(e)
        return {
            "message": "error"
        }


@order.route("/get", methods=["GET"])
def get_order():
    try:
        order_dict = json.loads(request.data)
        order_data = OrderItems.query.filter_by(order_id=order_dict.get("order_id")).all()
        # print(order_data[].order_id)
        order_list = []
        for order in order_data:
            order_list.append(
                {"order_items_id": order.order_items_id, "user_id": order.user_id, "quantity": order.quantity})
        return {
                   "order_id": order_dict.get("order_id"),
                   "data": order_list
               }, 200
    except Exception as e:
        logging.error(e)
        return {
            "message": str(e)
        }


@order.route("/delete", methods=["DELETE"])
def delete():
    try:
        request_data = json.loads(request.data)
        order_id = request_data.get("order_id")
        order_item = OrderItems.query.filter_by(order_id=order_id).all()
        for item in order_item:
            db.session.delete(item)
            db.session.commit()
        order_data = Orders.query.get(order_id)
        print(order_data.__dict__)
        db.session.delete(order_data)
        db.session.commit()
        return {
            "message": "delete successfully"
        }
    except Exception as e:
        logging.error(e)
        return {
            "error_message": str(e)
        }

