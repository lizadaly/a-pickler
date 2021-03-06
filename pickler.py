from pathlib import Path
import json
import string

from dictionary import WordList

mapping: dict[str, str] = {}
punctuation = list[str]


def normalize_dictionary(words: WordList) -> None:
    for word_group in words:
        word, correction, is_corrected = word_group
        if is_corrected and word != correction:
            mapping[correction.lower()] = word.lower()


def strip_punctation(line: str) -> tuple[str, str]:
    """Strip punctuation from a line, returning the removed punctuation and the updated line"""
    punct = str.maketrans(
        dict.fromkeys("'!\"#$%&'()*+,./:;<=>?@[]^_`{|}~'’“”\\")
    )  # string.punctuation plus smart quotes minus hyphens
    non_punct = str.maketrans(dict.fromkeys(string.ascii_letters + string.digits + " "))
    alpha_only = line.translate(punct).replace("  ", " ")
    removed = line.translate(non_punct)
    return alpha_only, removed.strip()


def pickler(source: list[str]) -> tuple[list[str], list[str]]:
    normalize_dictionary(json.load(Path("dictionary.json").open()))
    output: list[str] = []
    punct: list[str] = []

    for line in source:
        line, line_punct = strip_punctation(line)
        if line_punct:
            punct.append(line_punct)
        words = line.split(" ")
        for i, word in enumerate(words):
            orig_case = word
            word = word.lower()

            if word in mapping:
                words[i] = mapping[word]
                # Preserve initial case
                if orig_case[0].isupper():
                    words[i] = mapping[word].capitalize()
        output.append(" ".join(words))
    return output, punct


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str)
    args = parser.parse_args()
    source = Path(args.source)
    output = pickler(source.open().readlines())
    for line in output:
        print(line)
