import time
import argparse
from helpers.connection import conn

import sys


def main(args):
    # TODO

    seller_info = ["name", "phone", "local", "domain", "passwd"]

    try:
        cur = conn.cursor()

        if len(args.property) == 0:

            sql = "SELECT name, phone, local, domain FROM seller WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                print("\nName: {}\nPhone Number: {}\nemail: {}@{}\n".format(row[0], row[1], row[2], row[3]))

        if len(args.property) == 2:
            if args.property[0] == "name":
                sql = "UPDATE seller SET name=%(value)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "value": args.property[1]})
                conn.commit()
                print("Update Complete!")

            elif args.property[0] == "phone":
                sql = "UPDATE seller SET phone=%(value)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "value": args.property[1]})
                conn.commit()
                print("Update Complete!")
            elif args.property[0] == "local":
                sql = "UPDATE seller SET local=%(value)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "value": args.property[1]})
                conn.commit()
                print("Update Complete!")
            elif args.property[0] == "domain":
                sql = "UPDATE seller SET domain=%(value)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "value": args.property[1]})
                conn.commit()
                print("Update Complete!")
            elif args.property[0] == "passwd":
                sql = "UPDATE seller SET passwd=%(value)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "value": args.property[1]})
                conn.commit()
                print("Update Complete!")
            else:
                print("Error: Not valid property (Properties of seller are phone, local, domain, passwd)")
                print(
                    "You have to command like \
                    \n python seller.py ID \
                    \n python seller.py ID [property] [value]"
                )
        elif len(args.property) != 0:
            print(
                "Error: You have to command like \
                    \n python seller.py ID \
                    \n python seller.py ID [property] [value]"
            )

            sys.exit()

    except Exception as err:
        print(err)


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
