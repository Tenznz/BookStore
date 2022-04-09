def get_format(list_tuple):
    order_list = []
    for j in list_tuple:
        order_list.append((j[10], j[9], j[7]))
    order_list = list(set(order_list))
    mylist = list()
    for x in range(0, len(order_list)):
        order_dict = dict()
        new_list = []
        bo_id = order_list[x][0]
        for i in list_tuple:
            if int(bo_id) == int(i[5]):
                a = {
                    "book_id": i[0],
                    "quantity": i[15],
                    "book_name": i[1],
                }
                new_list.append(a)
        order_dict.update({
            "order_id": bo_id,
            "total_quantity": order_list[x][1],
            "total_price": order_list[x][2],
            "order_items": new_list
        })
        mylist.append(order_dict)
    return mylist
