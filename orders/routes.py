import json
import logging

import psycopg2
from flask import Blueprint, request

from orders.utils import get_format

logging.basicConfig(filename='order.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
orders = Blueprint("orders", __name__, url_prefix='/orders')
conn = psycopg2.connect("dbname=bookstore user=postgres password=1234")

cur = conn.cursor()


@orders.route("/get", methods=["GET"])
def get():
    try:
        order_data = json.loads(request.data)
        user_id = order_data.get('user_id')
        cur.execute(f"select * from books b,orders o,order_items oi where b.book_id=oi.book_id and "
                    f"oi.order_id=o.order_id and oi.user_id={user_id}")

        conn.commit()
        list_order = cur.fetchall()
        print(list_order)
        if not list_order:
            return {
                "message": "user_id not found"
            }
        order_info = get_format(list_order)

        return {
            "user_id": user_id,
            "order_list": order_info
        }
    except Exception as e:
        logging.error(e)
        return {
            "message": str(e)
        }


@orders.route("/add", methods=["POST"])
def post():
    try:
        order_dict = json.loads(request.data)
        user_id = order_dict.get("user_id")
        order_id = order_dict.get("order_id")
        status = order_dict.get("status")
        book_dic = order_dict.get("book_list")
        total_price = order_dict.get("total_price")
        total_quantity = sum(book_dic.values())
        cur.execute("insert into orders (order_id,user_id,total_quantity,total_price,status) values(%s,%s,%s,%s,%s)",
                    (order_id, user_id, total_quantity, total_price, status))
        conn.commit()
        # print("1")
        for i in book_dic:
            print(i)
            cur.execute("insert into order_items (book_id,user_id,quantity,order_id) values(%s,%s,%s,%s)",
                        (int(i), user_id, book_dic[i], order_id))
            conn.commit()
        return {
            "message": "successfully"
        }
    except Exception as e:
        logging.error(e)
        return {
            "message": "unsuccessfully"
        }


@orders.route("/delete", methods=["DELETE"])
def delete():
    try:
        order_data = json.loads(request.data)
        order_id = order_data.get('order_id')
        cur.execute(f"select order_items_id,book_id from order_items where order_id={order_id};")
        conn.commit()
        order_tuple = cur.fetchall()
        if len(order_tuple) == 0:
            return {
                "order_id": order_id,
                "message": "data not found"
            }
        cur.execute(f"delete from order_items where order_id = {order_id}")
        cur.execute(f"delete from orders where order_id={order_id}")
        conn.commit()

        return {
            "message": "delete successfully"
        }
    except Exception as e:
        logging.error(e)
        return {
            "message": str(e)
        }


@orders.route("/orderid", methods=["GET"])
def get_order_id():
    try:
        order_id = json.loads(request.data)["order_id"]
        print(order_id)
        cur.execute(f"select order_id,total_price,total_quantity from orders where order_id={order_id}")
        conn.commit()
        order_list = cur.fetchall()
        return {
            "message": "get data successfully",
            "data": {
                "order_id": order_list[0][0],
                "total_price": order_list[0][1],
                "total_quantity": order_list[0][2]
            }
        }
    except Exception as e:
        logging.error(e)
        return {
            "message": "data not found"
        }
