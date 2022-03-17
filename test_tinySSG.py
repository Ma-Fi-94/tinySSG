import pytest

from tinySSG import abort
from tinySSG import replace_extension
from tinySSG import replace_defines

def test_abort():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        abort("abcdefg")
    assert pytest_wrapped_e.type == SystemExit


def test_replace_extension():
	assert(replace_extension("abcde.old", "old", "new") == "abcde.new")


def test_replace_defines():
	input_string = '''#globaldefine VAR "content"
VAR'''
	correct_output = '''content'''
	assert(replace_defines(input_string) == correct_output)
