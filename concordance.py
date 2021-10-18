# Read through each word in `a-pickle.txt` and for each word:
# * Check against a spelling dictionary
# * If misspelled or unknown, suggest a spelling
# * Store the concordance
#
# The source will have little punctuation but retain all punctuation anyway
import tempfile
from pathlib import Path
import json


def generate_concordance_file(input_filename: str, output_filename: str):
    with Path(input_filename).open() as input, Path(output_filename).open(
        "w"
    ) as output:
        buffer: list[tuple[str, str]] = []
        for line in input:
            for word in line.split(" "):
                buffer.append((word, word))
        json.dump(buffer, output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="the function to call")
    args = parser.parse_args()

    if args.function == "generate":
        generate_concordance_file(
            input_filename="a-pickle-for-the-knowing-ones.txt",
            output_filename="concordance.json",
        )
