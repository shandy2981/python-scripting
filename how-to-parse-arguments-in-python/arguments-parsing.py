import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Learn how to parse arguments in python")

    parser.add_argument(
        'arg1',
        type=str,
        help="This is the first argument which is string type"
    )

    parser.add_argument(
        'arg2',
        type=int,
        default=10,
        help="The 2nd argument only accepts integers, default value is 10"
    )

    return parser.parse_args()

def display_arguments(arg1, arg2):
    return print(f"Arguments you have passed are: {arg1}, {arg2}")

def main():
    args = parse_args()
    display_arguments(args.arg1, args.arg2)

if __name__ == main():
    main()