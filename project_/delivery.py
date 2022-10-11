import time
import argparse
from helpers.connection import conn

import sys
from datetime import datetime

def main(args):
    # TODO

    try:
        cur = conn.cursor()
    
        if args.all == False and args.order_id == None:
            sql = "SELECT O.id, S.sname, O.cphone, O.menu, O.status, O.dtime FROM orders O, store S WHERE O.did=%(did)s and O.status=%(status)s and O.sid=S.id ORDER BY O.otime;"
            cur.execute(sql, {"did":args.id, "status": 1})

        elif args.all == True and args.order_id == None:
            sql = "SELECT O.id, S.sname, O.cphone, O.menu, O.status, O.dtime FROM orders O, store S WHERE O.did=%(did)s  and O.sid=S.id ORDER BY O.otime;"
            cur.execute(sql, {"did":args.id})

        elif args.all == False and args.order_id != None:    
            dtime = datetime.now()

            sql = "UPDATE orders SET status = %(status)s, dtime= %(dtime)s WHERE id=%(oid)s and did=%(did)s;"
            cur.execute(sql, {"status": 2, "dtime":dtime, "oid": args.order_id, "did":args.id})
            conn.commit()

            sql = "UPDATE delivery SET stock = stock-1 WHERE id=%(did)s;"
            cur.execute(sql, {"did":args.id})
            conn.commit()

            print("Deliver Completed!")
            sys.exit()

        else:
            print("Error: You have to command like this:\
                \npython delivery.py ID [ORDER_ID] [-a(--all)]")
            sys.exit()

        
        rows = cur.fetchall()

        if len(rows) == 0:
            print('Deliver {} has no food to deliver'.format(args.id))
            sys.exit()

        count = 0
        for row in rows:
            count = count + 1
            
            orderid, storename, customerphone, menu, status, dtime = row[0], row[1], row[2], row[3], row[4], row[5]
        
            print("\nOrder ID: {}\nMenu: {}\nStore: {}\nCustomer Phone Number: {}".format(orderid, menu, storename, customerphone))

            if int(status) == 1:
                print("Status: Delivering")

            else:
                print("Status: Delivered\nDelivered Time: {}".format(dtime))


    except Exception as err:
        print(err)




if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Delivery")
    parser.add_argument("order", help="order")
    parser.add_argument("-a", "--all", action="store_true", help="Display All orders")
    parser.add_argument("order_id", nargs="?", help="Deliverying order_id for changing to devliered")

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
