import re, sys, pathlib

def abort(message: str) -> None:
    '''Abort program execution after printing error message to stderr'''
    print(message, file=sys.stderr)
    raise SystemExit


def read_file(filepath: str) -> str:
    '''Generic file reading function'''
    filecontents = pathlib.Path(filepath).read_text()

    if len(filecontents) == 0:
        abort("File >>>" + filepath + "<<< has zero length. Aborting.")

    return filecontents


def write_file(destination: str, contents: str) -> None:
    '''Generic file writing function'''
    pathlib.Path(destination).write_text(contents)



def add_includes(raw: str) -> str:
    # Local copy to operate on
    ret = str(raw)
    
    # The pattern indicating a file include
    # We need to use parentheses to denote the matched group nb. 1
    include_pattern = r"^#include (.+)$"

    # Substitute all occurences at once with re.sub() and a substitution function
    f = lambda include_name: read_file(include_name.group(1))
    ret = re.sub(include_pattern, f, ret, flags=re.MULTILINE)

    # FIXME: Reading from file adds a newline at the end by default
    # FIXME: We might want to fix this, but it's not a major problem ATM.

    return ret


if __name__ == "__main__":  # pragma: no cover
    # python3 tinySSG.py --file inputfile outputfile
    # python3 tinySSG.py --folger path/to/folder inputextension outputextension
    
    
    if len(sys.argv) == 4 and sys.argv[1] == "--file":
        # Single-file mode
        inputfile = sys.argv[2]
        outputfile = sys.argv[3]

        # Load and process input file; write to HDD.
        raw = read_file(inputfile)
        processed = add_includes(raw)
        write_file(outputfile, processed)

    elif len(sys.argv) == 5 and sys.argv[1] == "--folder":
        # Whole-folder mode
        inputfolder = sys.argv[2]
        inputfile_extension = sys.argv[3]
        outputfile_extension = sys.argv[4]
        
        abort("Whole-folder mode is not implemented yet.")

    else:
        syntax = "\nSyntax:\n" + \
        "tinySSG.py --file inputfile outputfile\n" + \
        "tinySSG.py --folder path/to/folder inputextension outputextension\n"
        abort(syntax)
    
    
