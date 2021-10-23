from tinySSG import construct_destination_filename
from tinySSG import generate_site
from tinySSG import md_to_html
from tinySSG import load_config
from tinySSG import read_file
from tinySSG import write_file
from tinySSG import abort
from tinySSG import read_record

import io
import mock
import pytest
import sys



def test_read_record_missing_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_record("thispathdoesnotexist")
    assert pytest_wrapped_e.type == SystemExit


def test_abort():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        abort("abcdefg")
    assert pytest_wrapped_e.type == SystemExit


def test_load_config():
    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = ./template.html
    verbose = true
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        path_rawfiles, path_output, template_file, verbose = load_config(
            "dummypath")
    assert path_rawfiles == "./raw"
    assert path_output == "./public_html/"
    assert template_file == "./template.html"
    assert verbose == True

    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = ./template.html
    verbose = false
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        path_rawfiles, path_output, template_file, verbose = load_config(
            "dummypath")
    assert path_rawfiles == "./raw"
    assert path_output == "./public_html/"
    assert template_file == "./template.html"
    assert verbose == False


def test_load_config_emptyline():
    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = 
    path_output = ./public_html/
    template_file = ./template.html
    verbose = false
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = ./raw
    path_output = 
    template_file = ./template.html
    verbose = false
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = 
    verbose = false
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    [CONFIG]
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = ./template.html
    verbose =
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit


def test_load_config_nonsense():
    mock_configfile_content = '''
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = ./template.html
    verbose = abcde
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit


def test_load_config_missinglines():
    mock_configfile_content = '''
    path_output = ./public_html/
    template_file = ./template.html
    verbose = true
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    path_rawfiles = ./raw
    template_file = ./template.html
    verbose = true
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    path_rawfiles = ./raw
    path_output = ./public_html/
    verbose = true
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit

    mock_configfile_content = '''
    path_rawfiles = ./raw
    path_output = ./public_html/
    template_file = ./template.html
    '''
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_configfile_content),
                    create=True) as mock_file:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            path_rawfiles, path_output, template_file, verbose = load_config(
                "dummypath")
        assert pytest_wrapped_e.type == SystemExit


def test_read_file():
    mock_filecontents = "MOCKEDMOCKEDMOCKED\nMOCKEDMOCKEDMOCKEDMOCKED"
    with mock.patch("builtins.open",
                    mock.mock_open(read_data=mock_filecontents),
                    create=True) as mock_file:
        readfilecontents = read_file("dummypath")
    assert mock_filecontents == readfilecontents


def test_read_file_nonexisting_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        path_rawfiles, path_output, template_file, verbose = load_config(
            "dummypath")
    assert pytest_wrapped_e.type == SystemExit


def test_write_file():
    with mock.patch("builtins.open", mock.mock_open(),
                    create=True) as mock_file:
        write_file("dummypath", "content")

    mock_file.assert_called_once_with("dummypath", "w")
    mock_file.return_value.write.assert_called_once_with("content")


def test_write_file_IOError():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch("builtins.open", mock.mock_open(),
                        create=True) as mocked_open:
            mocked_open.side_effect = IOError()
            write_file("dummypath", "content")

    assert pytest_wrapped_e.type == SystemExit


def test_construct_destination_filename():
    assert construct_destination_filename(
        filename="filename.md", path_output="path/to/outputfolder"
    ) == "path/to/outputfolder/filename.html"
    assert construct_destination_filename(
        filename="filename.md", path_output="path/to/outputfolder/"
    ) == "path/to/outputfolder/filename.html"


def test_generate_site():
    assert generate_site(template = "{{.var1}} {{.content}}",
                         metadata = {"var1": "variable1text"},
                         content_md="contentcontent") == \
            "variable1text <p>contentcontent</p>"


def test_generate_site_missing_metadata():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        generate_site(template="{{.var1}} {{.content}}",
                      metadata={},
                      content_md="contentcontent")
    assert pytest_wrapped_e.type == SystemExit


def test_generate_site_no_content_tag():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        generate_site(template="{{.var1}}",
                      metadata={"var1": "variable1text"},
                      content_md="contentcontent")
    assert pytest_wrapped_e.type == SystemExit


def test_md_to_html():
    assert md_to_html("#heading") == "<h1>heading</h1>"
    assert md_to_html("# heading") == "<h1>heading</h1>"


def test_md_to_html_invalid_markdown():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        md_to_html(12345)
    assert pytest_wrapped_e.type == SystemExit
