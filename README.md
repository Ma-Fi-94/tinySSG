# tinySSG
A tiny static site generator / text processor (e.g. for blogging) I am currently writing

Currently, two features are implemented:
  - Include the content of another file: _#include filename_
  - Define a variable that gets replaced globally, i.e. throughout the whole file including all the lines before the definition: _#globaldefine VARNAME "variable content"_

# Usage
Two modes of operation are possible:
  - Singe-file mode: _tinySSG.py --file inputfile outputfile_
  - Whole-folder mode: tinySSG.py --folder path/to/folder inputextension outputextension

