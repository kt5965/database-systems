import time
import argparse
from helpers.connection import conn

import sys
from datetime import datetime
from geopy.distance import geodesic
import json


def main(args):
    # TODO
    
    try:
        cur = conn.cursor()

        if len(args.property) == 0:
            sql = "SELECT * FROM customer WHERE id=%(id)s ORDER BY id;"
            cur.execute(sql, {"id": args.id})    
            rows = cur.fetchall()
            print('Information of Customer {}'.format(args.id))
            print('-------------------------------------------------------------------')

            for row in rows:
                print('Name: {}\nPhone Number: {}\nE-mail: {}@{}\nNumber of payments: {}\nLatitude: {}\nLongitude: {}'.format(row[1],row[2], row[3],row[4],len(row[6]),row[7],row[8])) 

            print('-------------------------------------------------------------------\n')
        else:
            if args.property[0] == 'address':

                
                if len(args.property) == 1:                 # python customer.py ID address
                    sql = "SELECT address FROM address WHERE cid=%(cid)s ORDER BY id;"
                    cur.execute(sql, {"cid": args.id})                   
                    rows = cur.fetchall()
                    if len(rows) == 0:
                        print('The customer doesn\'t have address')
                    else:
                        print('Address of Customer {}'.format(args.id))
                        print('-------------------------------------------------------------------')                        
                        for rowindex in range(len(rows)):
                            print("{}. ".format(rowindex+1), end='')
                            print(rows[rowindex][0])
                        print('-------------------------------------------------------------------\n')                            

                else:
                    if args.property[1] == '-c' or args.property[1] == '--create':
                        for newaddress in args.property[2:]:
                            sql = "INSERT INTO address (cid, address) VALUES (%(cid)s, %(address)s);"
                            cur.execute(sql, {"cid": args.id,  "address":newaddress})
                            conn.commit()
                        print('Insertion complete!')


                    elif args.property[1] == '-e'or args.property[1] == '--edit':
                        if len(args.property) == 4:
                            sql = "UPDATE address SET address=%(address)s WHERE id = \
                                (SELECT A2.id FROM address AS A2 WHERE A2.cid=%(cid)s ORDER BY A2.id LIMIT 1 OFFSET %(n)s);"
                            cur.execute(sql, {"cid":args.id, "n": int(args.property[2])-1, "address": args.property[3]})
                            conn.commit()
                            print('Update complete!')

                        else:
                            print('You can modify only one address for one command.')

                    elif args.property[1] == '-r' or args.property[1] == '--remove':
                        if len(args.property) == 3:
                            sql = "DELETE FROM address WHERE id = \
                            (SELECT id FROM address WHERE cid=%(cid)s ORDER BY id LIMIT 1 OFFSET %(n)s);"
                            cur.execute(sql, {"cid":args.id, "n": int(args.property[2]) - 1})
                            conn.commit()
                            print('Removal complete')
                        else:
                            print('You can delete only one address for one command.')                            


                    else:
                        print('OPTIONS are -c(--create), -e(--edit), -r(--remove)')



            elif args.property[0] == 'pay':

                if len(args.property) == 1:                 # python customer.py ID address
                    sql = "SELECT aid, account_num, card_num FROM pay WHERE cid=%(cid)s ORDER BY aid, id;"
                    cur.execute(sql, {"cid": args.id})                   
                    rows = cur.fetchall()
                    if len(rows) == 0:
                        print('The customer doesn\'t have payment information')
                    else:

                        print('\nPrint payment information of customer {}'.format(args.id))
                        print('---------------------------------------------------------')

                        for rowindex in range(len(rows)):

                            print("\n{}.".format(rowindex+1))
                            if rows[rowindex][0] == 0:                      # Information of card
                                print('Type: Card')
                                print('Card number: {}'.format(rows[rowindex][2]))
                            else:                                           # Information of accounts
                                sql = 'SELECT name FROM bank WHERE id=%(aid)s;'
                                cur.execute(sql, {"aid":rows[rowindex][0]})
                                bank = cur.fetchall()[0][0]
                                

                                print('Type: Account')
                                print('Bank: {}'.format(bank))
                                print('Account number: {}'.format(rows[rowindex][1]))
                            #print(rows[rowindex][0])

                        print('---------------------------------------------------------')

                else:
                    if args.property[1] == '--add-card':
                        if len(args.property) == 2:
                            print('Error: there is no card number in command')
                            sys.exit()

                        # Check card number
                        for newcard in args.property[2:]:
                            if int(newcard) < 10**13 or int(newcard) >= 10**16:
                                print('Error: card number should be 14,15,16 digits.')
                                sys.exit()

                        for newcard in args.property[2:]:
                            sql = "INSERT INTO pay (cid, aid, card_num) VALUES(%(cid)s, %(aid)s, %(card_num)s);"
                            cur.execute(sql, {'cid': args.id, 'aid': 0, 'card_num': newcard})
                            conn.commit()
                        print('Insertion Complete!')


                    elif args.property[1] == '--add-account':
                        
                        if int(args.property[2]) < 1 or int(args.property[2]) > 19:
                            print("Error: bid has to be a number between 1 and 19")

                        else:
                            if len(args.property) == 3:
                                print('Error: there is no account number in command')
                            elif len(args.property) > 4:
                                print('Error: there are too many arguments')
                        
                            else:
                                sql = "INSERT INTO pay (cid, aid, account_num) VALUES(%(cid)s, %(aid)s, %(account_num)s);"
                                cur.execute(sql, {'cid': args.id, 'aid': args.property[2], 'account_num': args.property[3]})
                                conn.commit()                                                                
                                print('Insertion Complete')


                    elif args.property[1] == '-r' or args.property[1] == '--remove':

                        if len(args.property) == 3:
                            sql = "DELETE FROM pay WHERE id = \
                            (SELECT id FROM pay WHERE cid=%(cid)s ORDER BY aid,id LIMIT 1 OFFSET %(n)s);"
                            cur.execute(sql, {"cid":args.id, "n": int(args.property[2]) - 1})
                            conn.commit()
                            print('Removal complete')
                        else:
                            print('You can delete only one address for one command.')                         


                    else:
                        print('OPTIONS are --add-card, --add-account, -r(--remove)')


            elif args.property[0] == 'store':
                
                if len(args.property) == 2:
                    
                    now = datetime.now()
                    nowtime = int(str(now.hour)+str(now.minute))
                    nowday = now.weekday()

                    sql = 'SELECT schedules FROM store WHERE id = %(sid)s;'
                    cur.execute(sql, {"sid": args.property[1]})
                    rows = cur.fetchall()
                    for row in rows:
                        if row[0][nowday]['holiday'] == True:                   # The store is on holiday
                            
                            cur.execute('UPDATE customer SET lookat=%(value)s WHERE id=%(cid)s;', {"cid": args.id, "value": 0})
                            conn.commit()

                            print('Store {} is not open now'.format(args.property[1]))
                    
                        else:   
                            if int(row[0][nowday]['open']) < int(row[0][nowday]['closed']):
                                
                                if nowtime >= int(row[0][nowday]['open']) and nowtime <= int(row[0][nowday]['closed']):     # daytime-open store
                
                                    print('Menu of Store {}'.format(args.property[1]))
                                    print('------------------------------------------')
                                    
                                    cur.execute('UPDATE customer SET lookat=%(value)s WHERE id=%(cid)s;', {"cid": args.id, "value": args.property[1]})
                                    conn.commit()                                    
                                    sql = 'SELECT menu FROM menu WHERE sid=%(sid)s ORDER BY id;'
                                   
                                    cur.execute(sql, {"sid": args.property[1]})
                                    menus = cur.fetchall()
                
                                    for menuindex in range(len(menus)):
                                        print("#{}. ".format(menuindex + 1), end='')
                                        print(menus[menuindex][0]) 


                                else:

                                    cur.execute('UPDATE customer SET lookat=%(value)s WHERE id=%(cid)s;', {"cid": args.id, "value": 0})
                                    conn.commit()  
                                    print('Store {} is not open now'.format(args.property[1]))                                    

                            else:                           
                                # midnight-open store
                                if nowtime >= max(int(row[0][nowday]['open']), int(row[0][nowday]['closed'])) or nowtime <= min(int(row[0][nowday]['open']), int(row[0][nowday]['closed'])):
                                    print('Menu of Store {}'.format(args.property[1]))
                                    print('------------------------------------------')

                                    cur.execute('UPDATE customer SET lookat=%(value)s WHERE id=%(cid)s;', {"cid": args.id, "value": args.property[1]})
                                    conn.commit()  

                                    sql = 'SELECT menu FROM menu WHERE sid=%(sid)s ORDER BY id;'
                                    cur.execute(sql, {"sid": args.property[1]})
                                    menus = cur.fetchall()
                
                                    for menuindex in range(len(menus)):
                                        print("#{}. ".format(menuindex + 1), end='')
                                        print(menus[menuindex][0])                  

                                    print('-----------------------------------------')

                                else:

                                    print('Store {} is not open now'.format(args.property[1]))


                elif len(args.property) > 2:                       # python customer.py ID store [-a|-o|-l] [OPTIONS]
                    checkOptionA = False
                    checkOptionO = -1
                    numData = 10

                    if '-a' in args.property[1:]:
                        checkOptionA = True

                    for argindex in range(1, len(args.property)):
                        if args.property[argindex] == '-o':
                            if argindex < len(args.property)-1 and args.property[argindex + 1] in ['0', '1', '2', 'name', 'address', 'distance']:
                                if args.property[argindex+1] == '0' or args.property[argindex+1] == 'name':
                                    checkOptionO = 0
                                elif args.property[argindex+1] == '1' or args.property[argindex+1] == 'address':
                                    checkOptionO = 1
                                else:
                                    checkOptionO = 2

                            else:
                                print('Option is 0(name), 1(address), 2(distance)')
                                sys.exit()

                        elif args.property[argindex] == '-l':
                            if argindex < len(args.property)-1:
                                numData = int(args.property[argindex+1])

                    
                    if checkOptionA == True:
                        if checkOptionO == 0:
                            sql = 'SELECT id, sname, address, phone_nums FROM store ORDER BY sname, id LIMIT %(limit)s;'
                            cur.execute(sql, {"limit": numData})
                            stores = cur.fetchall()

                            print('---------------------------------------------------')
                            for store in stores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(store[0], store[1], store[2], store[3]))
                            print('---------------------------------------------------')

                        elif checkOptionO == 1:

                            sql = 'SELECT id, sname, address, phone_nums FROM store ORDER BY REPLACE(address,\' \', \'\'), id LIMIT %(limit)s;'
                            cur.execute(sql, {"limit": numData})
                            stores = cur.fetchall()

                            print('---------------------------------------------------')
                            for store in stores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(store[0], store[1], store[2], store[3]))
                            print('---------------------------------------------------')

                            pass

                        elif checkOptionO == 2:


                            cur.execute('SELECT lat, lng from customer where id=%(cid)s;', {"cid":args.id})
                            cgeo = cur.fetchall()[0]
                            clat = cgeo[0]
                            clng = cgeo[1]

                            cur.execute('SELECT id, sname, address, phone_nums, lat, lng FROM store;')
                            stores = cur.fetchall()
                            
                            sortedstores = sorted(stores, key = lambda x: geodesic((clat, clng), (x[4], x[5])))[:numData]

                            print('---------------------------------------------------')
                            for sortedstore in sortedstores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(sortedstore[0], sortedstore[1], sortedstore[2], sortedstore[3]))
                            print('---------------------------------------------------')                            
                            
                        else:
                            pass
                    else:
                        if checkOptionO == 0:
                            pass

                            sql = 'SELECT id, sname, address, phone_nums, schedules FROM store ORDER BY sname, id'
                            cur.execute(sql)
                            stores = cur.fetchall()
                           
                            now = datetime.now()
                            nowtime = int(str(now.hour)+str(now.minute))
                            nowday = now.weekday()                            

                            count = 0
                            nstores = []

                            for store in stores:
                                if count == numData:
                                    break

                                if store[4][nowday]['holiday'] == True:                   # The store is on holiday
                                    continue
                                
                                else:   
                                    if int(store[4][nowday]['open']) < int(store[4][nowday]['closed']):
                               
                                        if nowtime >= int(store[4][nowday]['open']) and nowtime <= int(store[4][nowday]['closed']):     # daytime-open store
                                            count = count + 1
                                            nstores.append(store)
                                            
                                        else: 
                                            continue
                                    else:                           
                                            # midnight-open store
                                        if nowtime >= max(int(store[4][nowday]['open']), int(store[4][nowday]['closed'])) or nowtime <= min(int(store[4][nowday]['open']), int(store[4][nowday]['closed'])):
                                            count = count + 1
                                            nstores.append(store)

                                        else:
                                            continue                           


                            print('---------------------------------------------------')
                            for nstore in nstores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(nstore[0], nstore[1], nstore[2], nstore[3]))
                            print('---------------------------------------------------')



                        elif checkOptionO == 1:

                            sql = 'SELECT id, sname, address, phone_nums, schedules FROM store ORDER BY address, id'
                            cur.execute(sql)
                            stores = cur.fetchall()
                           
                            now = datetime.now()
                            nowtime = int(str(now.hour)+str(now.minute))
                            nowday = now.weekday()                            

                            count = 0
                            nstores = []

                            for store in stores:
                                if count == numData:
                                    break

                                if store[4][nowday]['holiday'] == True:                   # The store is on holiday
                                    continue
                                
                                else:   
                                    if int(store[4][nowday]['open']) < int(store[4][nowday]['closed']):
                               
                                        if nowtime >= int(store[4][nowday]['open']) and nowtime <= int(store[4][nowday]['closed']):     # daytime-open store
                                            count = count + 1
                                            nstores.append(store)
                                            
                                        else: 
                                            continue
                                    else:                           
                                            # midnight-open store
                                        if nowtime >= max(int(store[4][nowday]['open']), int(store[4][nowday]['closed'])) or nowtime <= min(int(store[4][nowday]['open']), int(store[4][nowday]['closed'])):
                                            count = count + 1
                                            nstores.append(store)

                                        else:
                                            continue                           


                            print('---------------------------------------------------')
                            for nstore in nstores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(nstore[0], nstore[1], nstore[2], nstore[3]))
                            print('---------------------------------------------------')



                        elif checkOptionO == 2:



                            cur.execute('SELECT lat, lng from customer where id=%(cid)s;', {"cid":args.id})
                            cgeo = cur.fetchall()[0]
                            clat = cgeo[0]
                            clng = cgeo[1]

                            cur.execute('SELECT id, sname, address, phone_nums, schedules, lat, lng FROM store;')
                            stores = cur.fetchall()
                            
                            sortedstores = sorted(stores, key = lambda x: geodesic((clat, clng), (x[5], x[6])))

                            now = datetime.now()
                            nowtime = int(str(now.hour)+str(now.minute))
                            nowday = now.weekday()   


                            count = 0
                            nstores = []

                            for sortedstore in sortedstores:

                                if count == numData:
                                    break

                                if sortedstore[4][nowday]['holiday'] == True:                   # The store is on holiday
                                    continue
                                
                                else:   
                                    if int(sortedstore[4][nowday]['open']) < int(sortedstore[4][nowday]['closed']):
                               
                                        if nowtime >= int(sortedstore[4][nowday]['open']) and nowtime <= int(sortedstore[4][nowday]['closed']):     # daytime-open store
                                            count = count + 1
                                            nstores.append(sortedstore)
                                            
                                        else: 
                                            continue
                                    else:                           
                                            # midnight-open store
                                        if nowtime >= max(int(sortedstore[4][nowday]['open']), int(sortedstore[4][nowday]['closed'])) or nowtime <= min(int(sortedstore[4][nowday]['open']), int(sortedstore[4][nowday]['closed'])):
                                            count = count + 1
                                            nstores.append(sortedstore)

                                        else:
                                            continue                            


                            print('---------------------------------------------------')
                            for nstore in nstores:
                                print("\nStore ID: {}\nname: {}\naddress: {}\nphone number: {}\n".format(nstore[0], nstore[1], nstore[2], nstore[3]))
                            print('---------------------------------------------------')


                        else:
                            pass

                    
            elif args.property[0] == 'cart':
                print

                if len(args.property) == 1:
                    sql = 'SELECT lookat FROM customer WHERE id=%(id)s;'
                    cur.execute(sql, {"id":args.id})
                    lookat = cur.fetchall()[0][0]

                    if lookat == 0 or lookat == None:
                        print('Select store first') 
                        sys.exit()

                    else:
                        sql = 'SELECT id, menu FROM menu WHERE sid=%(sid)s ORDER BY id';
                        cur.execute(sql, {"sid": lookat})
 
                        menus = cur.fetchall()
                        menutable = []

                        print("Menus of Store {}".format(lookat))
                        print('------------------------------------')
                        for menuIndex in range(0,len(menus)):
                            print("{}. ".format(menuIndex+1), end='')
                            print(menus[menuIndex][1])
                            menutable.append(menus[menuIndex][0])

                        print('------------------------------------')

                else:
                    sql = 'SELECT lookat FROM customer WHERE id=%(id)s;'
                    cur.execute(sql, {"id":args.id})
                    lookat = cur.fetchall()[0][0]

                    if lookat == 0 or lookat == None:
                        print('Select store first') 
                        sys.exit()          

                    else:
                        sql = 'SELECT id, menu FROM menu WHERE sid=%(sid)s ORDER BY id;'
                        cur.execute(sql, {"sid": lookat})
 
                        menus = cur.fetchall()
                        menutable = []

                        for menuIndex in range(0,len(menus)):
                            menutable.append(int(menus[menuIndex][0]))


                    if args.property[1] == '-c':
                        for argIndex in range(2, len(args.property)):
                            

                            if argIndex % 2 == 0 and argIndex < len(args.property) - 1:
                                sql = 'INSERT INTO cart (cid, mid, count) VALUES (%(cid)s, %(mid)s, %(count)s);'
                                cur.execute(sql, {"cid": args.id, "mid": menutable[int(args.property[argIndex]) - 1], "count": args.property[argIndex+1]})
                                conn.commit()

                        print('Insertion Complete!')
                            

                    elif args.property[1] == '-l':
                        cur.execute('SELECT M.menu, C.count FROM menu M, cart C WHERE C.cid=%(cid)s AND M.id=C.mid ORDER BY C.id;', {"cid":args.id})
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            print('Cart is empty')
                            sys.exit()
                        else:
                            print("Cart of Custommer {}".format(args.id))
                            print("---------------------------------------------------")
                            for rowIndex in range(0, len(rows)):
                                print("{}. Menu: {},  Counts: {}".format(rowIndex+1,rows[rowIndex][0], rows[rowIndex][1]))
                            print("---------------------------------------------------")
                                

                    elif args.property[1] == '-r':

                        if len(args.property) == 3:
                            sql = "DELETE FROM cart WHERE id = \
                            (SELECT id FROM cart WHERE cid=%(cid)s ORDER BY id LIMIT 1 OFFSET %(n)s);"
                            cur.execute(sql, {"cid":args.id, "n": int(args.property[2]) - 1})
                            conn.commit()
                            print('Removal complete')                            


                    elif args.property[1] == '-p':


                        if len(args.property) == 3:

                            sql = "SELECT M.id, M.menu, M.sid, C.count FROM cart C, menu M WHERE C.cid = %(cid)s AND C.mid = M.id;"
                            cur.execute(sql, {"cid":args.id}) 
                            items = cur.fetchall()
                            if len(items) == 0:
                                print('There is no item in cart')
                                sys.exit()

                            sql = "SELECT payments FROM customer WHERE id=%(cid)s;"
                            cur.execute(sql, {"cid":args.id})
                            payinfo = cur.fetchall()[0][0]
                            

                            if len(payinfo) < int(args.property[2]):
                                print("Error: The Customer doesn't have {} payments".format(args.property[2]))
                                sys.exit()
                            
                            menu = []
                            for item in items:
                                menutuple = {}
                                menutuple['Name'] = item[1]
                                menutuple['Count'] = item[3]
                                menu.append(menutuple)



                            sql = "SELECT aid, account_num, card_num FROM pay WHERE id = \
                            (SELECT id FROM pay WHERE cid=%(cid)s ORDER BY aid,id LIMIT 1 OFFSET %(n)s);"
                            cur.execute(sql, {"cid":args.id, "n": int(args.property[2]) - 1})                            
                            payment = cur.fetchall()[0]
                            if len(payment) == 0:
                                print('There is no payment information')
                                sys.exit()


                            aid = payment[0]
                            account_num = payment[1]
                            card_num = payment[2]

                            paymentTuple = {}

                            if aid == 0:
                                paymentTuple['Type'] = 'Card'
                                paymentTuple['CardNum'] = card_num
                                                                                             
                            else:
                                paymentTuple['Type'] = 'Account'
                                paymentTuple['AccountNum'] = account_num

                            


                            sql = "SELECT phone FROM customer WHERE id=%(id)s;"
                            cur.execute(sql, {"id":args.id})
                            customerphone = cur.fetchall()[0][0]


                            ordertime = datetime.now()

                            sql = "INSERT INTO orders (cid, sid, mid, menu, payment, otime, cphone, status) VALUES \
                                (%(cid)s, %(sid)s, %(mid)s, %(menu)s, %(payment)s, %(otime)s, %(cphone)s, %(status)s);"
                            cur.execute(sql, {"cid": args.id, "sid": item[2], "mid": item[0], "menu": json.dumps(menu),\
                                 "payment": json.dumps(paymentTuple), "otime":ordertime, "cphone":customerphone, "status":0})   
                            conn.commit()


                            cur.execute("DELETE FROM cart WHERE cid=%(cid)s;", {"cid": args.id})
                            conn.commit()

                     
                        
                    else:
                        print('Options are -c, -l, -r, -p')
                        sys.exit()



            elif args.property[0] == 'order':                                

                if len(args.property) == 1:
                    sql = "SELECT O.id, S.sname, O.menu, O.status, O.otime, O.dtime FROM orders O, store S WHERE O.cid=%(cid)s AND O.sid=S.id ORDER BY O.otime;"
                    cur.execute(sql, {"cid": args.id})


                elif len(args.property) == 2 and (args.property[1] == '-w' or args.property[1] == '--waiting'):
                    sql = "SELECT O.id, S.sname, O.menu, O.status, O.otime, O.dtime FROM orders O, store S WHERE O.cid=%(cid)s AND O.status = %(status)s AND O.sid=S.id ORDER BY O.otime;"
                    cur.execute(sql, {"cid": args.id, "status": 1})

                else:
                    print("You have to command like \
                        \npython customer.py ID order \
                        \npython customer.py ID order [-w(--waiting)]")
                    sys.exit()

                orders = cur.fetchall()
                if len(orders) == 0:
                    print("There are no orders!")
                    sys.exit()

                count = 0
                for order in orders:
                    count = count + 1
                    orderid, storename, menu, status, otime, dtime = order[0], order[1], order[2], order[3], order[4], order[5]

                    print("\n{}.\nOrder ID: {}\nStore: {}\nMenu: {}\nOrder Time: {}".format(count, orderid, storename, menu, otime))
                    if int(status) == 0:
                        print("Status: Pending")

                    elif int(status) == 1:
                        print("Status: Delivering now")
                    else:
                        print("Status: Delivered when {}".format(dtime))

                
                
            else:
                print('Error: You have to command like \
                        \n python customer.py ID  \
                        \n python customer.py ID  address [OPTIONS] ARGS... \
                        \n python customer.py ID  pay [OPTIONS] ARGS... \
                        \n python customer.py ID  store SID \
                        \n python customer.py ID  store [-a|-o|-l] [OPTIONS] \
                        \n python customer.py ID  cart [OPTIONS] ...ARGS \
                        \n python customer.py ID  order [-w] ')                                                                    


    except Exception as err:
        print(err)


if __name__ == "__main__":

    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Customer")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Other properties: address, store, cart, order")    
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
