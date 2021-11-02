import tempfile
from dictionary import *
from pickler import *
from pathlib import Path


def test_pickler():
    """Passing text through the pickler should convert the words"""
    source = ["When the moon hits your eye like a big pizza pie"]
    output = " ".join(pickler(source)[0]).strip()
    assert "Wen the moune hits your eye lik a big pizza pie" == output


def test_extract_punctuation():
    """Punctuation from the source should be extracted and returned separately"""
    source = "It is a truth universally acknowledged, that a single man (??) loves punctuation!!"
    text, punct = strip_punctation(source)
    assert (
        "It is a truth universally acknowledged that a single man loves punctuation"
        == text
    )
    assert ",(??)!!" == punct


def test_extract_punctuation_appended():
    """In a complete source document, punctuation should be extracted and appended at the end"""
    source = [
        "It is a truth universally acknowledged, that a single man (??) loves punctuation!!"
    ]
    output = " ".join(pickler(source)[0])
    output += " " + " ".join(pickler(source)[1])
    assert (
        "Itt is a trouth universally acknowledged that a single man leovs punctuation ,(??)!!"
        == output
    )


def test_dictionary():
    """The dictionary generator should serialize the input in the expected format"""
    _, input_filename = tempfile.mkstemp()
    _, output_filename = tempfile.mkstemp()
    try:
        Path(input_filename).open("w").write(
            "To mankind at Large the time is Com at Last the grat day of Regoising"
        )
        generate_dictionary_file(input_filename, output_filename)
        out = json.load(open(output_filename))
        assert len(out) == 15
        assert len(out[0]) == 3
        assert out[0][0]
        assert out[0][0] == out[0][1]
        assert out[0][2] == False

    finally:
        Path(input_filename).unlink()
        Path(output_filename).unlink()
