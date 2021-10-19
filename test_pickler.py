import tempfile
from dictionary import *
from pathlib import Path


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
