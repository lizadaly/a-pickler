# Read through each word in `a-pickle.txt` and for each word:
# * Check against a spelling dictionary
# * If misspelled or unknown, suggest a spelling
# * Store the concordance
#

from pathlib import Path
import json
from typing import Optional
import pkg_resources
from symspellpy import SymSpell, Verbosity
from rich import print


def generate_concordance_file(input_filename: str, output_filename: str):
    with Path(input_filename).open() as input, Path(output_filename).open(
        "w"
    ) as output:
        buffer: list[tuple[str, Optional[str]]] = []
        for line in input:
            for word in line.split(" "):
                buffer.append((word, None))
        json.dump(buffer, output)


def spellcheck(concordance: Path):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    words = json.load(concordance.open())

    for word_pair in words:
        word, correction = word_pair
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        print(word)
        for s in suggestions:
            print(s)


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
    elif args.function == "spellcheck":
        spellcheck(Path("concordance.json"))
