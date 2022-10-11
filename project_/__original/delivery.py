import time
import argparse


def main(args):
    # TODO
    print(args)
    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Delivery")
    parser.add_argument("-a", "--all", action="store_true", help="Display All orders")
    parser.add_argument("order_id", nargs="?", help="Deliverying order_id for changing to devliered")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
