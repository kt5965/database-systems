import time
import argparse


def main(args):
    # TODO
    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
