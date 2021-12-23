# tinySSG
A tiny static site generator (e.g. for blogging) I am currently writing

# Invoking tinySSG
Configuration (verbosity setting, output path, path to the template HTML file, and path to the input markdown files to be converted to HTML files) goes into *tinySSG.ini*. Then, just run *tinySSG.py*. (You can completely ignore the test files and the build pipeline shell script.)

For every input file, a copy of the template file is made and its {{.content}} tag is replaced with the complete file contents of the input file.
