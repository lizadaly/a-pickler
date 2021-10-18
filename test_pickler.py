import tempfile
from concordance import *


def test_concordance():
    """The concordance generator should serialize the input in the expected format"""
    _, input_filename = tempfile.mkstemp()
    _, output_filename = tempfile.mkstemp()
    Path(input_filename).open("w").write(
        "To mankind at Large the time is Com at Last the grat day of Regoising"
    )
    generate_concordance_file(input_filename, output_filename)
    out = json.load(open(output_filename))
    assert len(out) == 15
    assert len(out[0]) == 2
    assert out[0][0] == out[0][1]