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
    if len(sys.argv) != 3:
        abort("\nSyntax:\ntinySSG.py inputfile outputfile\n")
    else:
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
    
    # Read input
    raw = read_file(inputfile)

    # Add all includes
    processed = add_includes(raw)
    
    # Write to destination
    write_file(outputfile, processed)
    
