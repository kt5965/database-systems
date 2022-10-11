import time
import argparse
from helpers.connection import conn

import sys
from geopy.distance import geodesic
from datetime import datetime

def main(args):
    # TODO

    store_info = ['sid', 'address', 'sname', 'lat', 'lng', 'phone_nums', 'schedules', 'seller_id', 'menus']    

    try:

        cur = conn.cursor()

        if len(args.property) == 0:

            sql = "SELECT sname, address, phone_nums, schedules, lat, lng, seller_id FROM store WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})    
            rows = cur.fetchall()
            for row in rows:
                print('\nStore ID: {}\nName: {}\nSeller ID: {}\naddress: {}\nPhone Number: {}\nLatitude: {}\nLongitude: {}'.format(args.id,row[0],row[6],row[1],row[2], row[4], row[5]))
                print('Schedule:')
                for dayindex in range(0, 6):
                    print('\t{}'.format(row[3][dayindex]))
            print('\n')

        else:

            if args.property[0] == 'menu':
                
                if len(args.property) == 1:
                    sql = "SELECT menu, id FROM menu where sid=%(id)s ORDER BY id;"
                    cur.execute(sql, {"id":args.id})
                    rows = cur.fetchall()
                    print('Menu of store {}'.format(args.id))
                    print('--------------------------------------')
                    for rowIndex in range(0,len(rows)):
                        print("{}. Menu ID: {}, Name: {} ".format(rowIndex+1, rows[rowIndex][1], rows[rowIndex][0]))

                    print('--------------------------------------\n')


                elif len(args.property) == 2:
                    sql = 'INSERT INTO menu (sid, menu) VALUES (%(id)s, %(menu)s);'
                    cur.execute(sql, {"id": args.id,  "menu":args.property[1]})
                    conn.commit()
                    print('Complete menu addition!')

                else:
                    print('Error: You have to command like \
                            \n python store.py ID menu  \
                            \n python store.py ID menu [NAME]')



            elif args.property[0] == 'order':


                if len(args.property) == 1:
                    sql = 'SELECT id, menu, cphone, otime,status FROM orders WHERE sid=%(sid)s ORDER BY otime;'
                    cur.execute(sql, {"sid":args.id})



                elif len(args.property) == 2:
                    if args.property[1] == '0' or args.property[1].upper() == 'PENDING':
                        sql = 'SELECT id, menu, cphone, otime, status FROM orders WHERE sid=%(sid)s AND status=%(status)s ORDER BY otime;'
                        cur.execute(sql, {"sid":args.id, "status": 0})

                    elif args.property[1] == '1' or args.property[1].upper() == 'DELIVERING':
                        sql = 'SELECT id, menu, cphone, otime, status FROM orders WHERE sid=%(sid)s AND status=%(status)s ORDER BY otime;'
                        cur.execute(sql, {"sid":args.id, "status": 1})                        

                    elif args.property[1] == '2' or args.property[1].upper() == 'DELIVERED':
                        sql = 'SELECT id, menu, cphone, otime, status FROM orders WHERE sid=%(sid)s AND status=%(status)s ORDER BY otime;'
                        cur.execute(sql, {"sid":args.id, "status": 2})                        



                    else:
                        try:
                            orderid = int(args.property[1])

                            sql = "SELECT status FROM orders WHERE id=%(oid)s;"
                            cur.execute(sql, {"oid": orderid})
                            status = cur.fetchall()

                            if len(status) == 0:
                                print("Store {} has no order of ID {}".format(args.id, orderid))
                                sys.exit()
                            


                            sql = "SELECT lat,lng FROM store WHERE id=%(sid)s;"
                            cur.execute(sql, {"sid":args.id})
                            sgeo = cur.fetchall()
                            slat, slng = sgeo[0][0], sgeo[0][1]
                            

                            cur.execute('SELECT lat, lng, stock, id, phone FROM delivery;')
                            deliveries = cur.fetchall()
                            
                            sorteddeliveries = sorted(deliveries, key = lambda x: geodesic((slat, slng), (x[0], x[1])))

                            did = -1

                            for delivery in sorteddeliveries:
                                if int(delivery[2]) <= 4:
                                    did = int(delivery[3])
                                    dphone = delivery[4]
                                    dlat, dlng, dstock, did, dphone = delivery[0], delivery[1], delivery[2], delivery[3], delivery[4]
                                    break
                            

                            if did == -1:
                                print("There are no deliveries whose stock <= 4.")
                                sys.exit()                                                        

                  
                        
                            sql = "UPDATE orders SET status=%(status)s, did=%(did)s WHERE id=%(orderid)s;"
                            cur.execute(sql,{"status": 1, "did":did, "orderid":orderid})
                            conn.commit()

                            sql = "UPDATE delivery SET stock = stock+1 WHERE id=%(did)s;"
                            cur.execute(sql, {"did":did})
                            conn.commit()


                            print("Complete!\nDelivery ID: {}\nDelivery Phone: {}\n".format(did,dphone))
                            sys.exit()
                        
                        except ValueError:
                            print('Invalid order ID: Order Id should be Integer')
                            sys.exit()

                else:
                    print('You have to command like this:\
                        \n\npython store.py ID order [FILTER]\
                        \npython store.py ID order ORDER_ID\
                        \n\nFilters are 0(PENDING), 1(DELIVERING), 2(DELIVERED)')
                    sys.exit()

                rows = cur.fetchall()
                print('Orders of store {}'.format(args.id))
                print('------------------------------------------------------------------------')

                for row in rows:
                    
                    orderid, customerphone, ordertime, status = row[0], row[2], row[3], row[4] 

                    print("\nOrder ID: {}\nOrder time: {}\nCustomer Phone Number: {}".format(orderid, ordertime, customerphone))

                    if int(status) == 0:
                        print("Status: Pending")
                    elif int(status) == 1:
                        print("Status: Delivering")
                    else:
                        print("Status: Delivered")

                    for menu in row[1]:
                        menuName = menu['Name']
                        menuCount = menu['Count']
                        print("Menu: {}, Count: {}".format(menuName, menuCount))      
                print('------------------------------------------------------------------------\n')              

            else:
                pass

    except Exception as err:
        print(err)

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Store")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Other properties: menu, order")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
