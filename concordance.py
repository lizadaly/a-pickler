# Read through each word in `a-pickle.txt` and for each word:
# * Check against a spelling dictionary
# * If misspelled or unknown, suggest a spelling
# * Store the concordance
#

from pathlib import Path
import json
from typing import Optional
import pkg_resources
from rich.text import Text
from symspellpy import SymSpell, Verbosity
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track
from rich.panel import Panel
from rich.layout import Layout
from rich import print

console = Console()
CONTEXT_BUFFER = 10


class OverridablePrompt(Prompt):
    """Allow unlisted options"""

    def check_choice(self, value: str) -> bool:
        return True


def generate_concordance_file(input_filename: str, output_filename: str):
    with Path(input_filename).open() as input, Path(output_filename).open(
        "w"
    ) as output:
        buffer: list[tuple[str, str, bool]] = []
        for line in input:
            for word in line.split(" "):
                buffer.append((word, word, False))
        json.dump(buffer, output)


def spellcheck(concordance: Path):

    words: list[tuple[str, str, bool]] = json.load(concordance.open())
    console.clear()
    try:
        check_words(words)
    finally:
        with concordance.open("w") as out:
            json.dump(words, out)


def check_words(words: list[tuple[str, str, bool]]):
    console.print("Loading spelling dictionary...")
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    for index, word_group in enumerate(words):
        word, _, corrected = word_group
        checkable_word = word.strip()
        if checkable_word.isalnum() and not corrected:
            suggestions = sym_spell.lookup(
                checkable_word,
                Verbosity.CLOSEST,
                max_edit_distance=2,
                transfer_casing=True,
            )

            context = Text()
            before = [w[1] for w in words[max(0, index - CONTEXT_BUFFER) : index]]
            after = [
                w[1]
                for w in words[index + 1 : min(len(words) - 1, index + CONTEXT_BUFFER)]
            ]
            context.append(" ".join(before).replace("\n", ""))
            context.append(Text(f" {checkable_word} ", style="bold magenta"))
            context.append(" ".join(after).replace("\n", ""))
            console.print(Panel(context))

            correction = OverridablePrompt.ask(
                f"[b]{word}[/b]: ",
                choices=[s.term for s in suggestions[:5]],
                default=suggestions[0].term,
            )
            words[index] = (word, correction, True)
            console.clear()


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
