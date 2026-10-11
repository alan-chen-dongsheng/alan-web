import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="输出传入的示例值")
    parser.add_argument("--value", required=True)
    args = parser.parse_args()
    print(args.value)


if __name__ == "__main__":
    main()
