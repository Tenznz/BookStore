def get_format(list_tuple):
    order_list = []
    for j in list_tuple:
        order_list.append((j[5], j[8], j[7]))
    print(order_list)
    order_list = list(set(order_list))
    mylist = list()
    for x in range(0, len(order_list)):
        order_dict = dict()
        new_list = []
        bo_id = order_list[x][0]
        for i in list_tuple:
            # print(i[5])
            if bo_id == i[5]:
                a = {
                    "book_id": i[0],
                    "quantity": i[13],
                    "book_name": i[1]
                }
                print(a)
                new_list.append(a)
        order_dict.update({
            "order_id": bo_id,
            "total_quantity": order_list[x][1],
            "total_price": order_list[x][2],
            "order_items": new_list
        })
        mylist.append(order_dict)
        # print(mylist)
    return mylist
