import argparse


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image",
                        help="Image directory")

    parser.add_argument('-d', '--debug',
                        nargs='?',
                        const=True,
                        help="Activate debug mode")
    args = parser.parse_args()
    return args
