import sys
import argparse
import select


##
# Retrieves command-line arguments using argparse.
##
def get_arguments(description):
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-i", "--input",
                        help="File path to read content from (or just read from standard input)",
                        type=str)
    return parser.parse_args()


##
# Reads content from a file or standard input.
##
def read_content(file_path=None):
    content = ""
    try:
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        else:
            # Check if there's input ready on stdin
            if select.select([sys.stdin], [], [], 0.0)[0]:
                content = sys.stdin.read()
            else:
                sys.exit("Error: No content provided on standard input.")
    except IOError as e:
        sys.exit(f"Error reading file: {e}")

    return content
