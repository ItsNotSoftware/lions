import sys


def main(msg_files_dir: str, output_dir: str):
    pass


if __name__ == "__main__":
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print("Usage: lions.main <msg_files_dir> <output_dir>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
