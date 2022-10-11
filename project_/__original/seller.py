import time
import argparse
from helpers.connection import conn


def main(args):
    # TODO
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": 2})
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as err:
        print(err)
    print(args)
    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
