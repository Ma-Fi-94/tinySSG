from tinySSG import construct_destination_filename
from tinySSG import generate_site

def test_construct_destination_filename():
    assert construct_destination_filename(filename = "filename.md", path_output="path/to/outputfolder") == "path/to/outputfolder/filename.html"
    assert construct_destination_filename(filename = "filename.md", path_output="path/to/outputfolder/") == "path/to/outputfolder/filename.html"

def test_generate_site():
    assert generate_site(template = "{{.var1}} {{.content}}",
                         metadata = {"var1": "variable1text"},
                         content_md="contentcontent") == \
            "variable1text <p>contentcontent</p>"
                        
