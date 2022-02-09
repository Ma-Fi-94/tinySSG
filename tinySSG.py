import re
import sys

def read_file(filepath: str) -> str:
    '''Generic file reading function'''
    try:
        with open(filepath, "r") as f:
            filecontents = f.read()
    except:
        print("Error loading file >>>" + filepath + "<<<. Aborting.")
        raise SystemExit
    
    if len(filecontents) == 0:
        print("File >>>" + filepath + "<<< has zero length. Aborting.")
        raise SystemExit

    return filecontents


def write_file(destination: str, contents: str) -> None:
    '''Generic file writing function'''
    try:
        with open(destination, "w") as f:
            f.write(contents)
    except:
        print("Error writing to file " + destination + ". Aborting.")
        raise SystemExit


def add_includes(raw: str) -> str:
    # Local copy to operate on
    ret = str(raw)
    
    # Get all occurences of the #include pattern
    include_pattern = r"^#include .+$"
    all_includes = re.findall(include_pattern, raw, re.MULTILINE)
    
    # Iterate through them
    for include in all_includes:
        # Extract filename from pattern
        filename = include.split("#include ")[1]
        
        # Try to load the file
        # FIXME: Reading from file adds a newline at the end by default
        # FIXME: We might want to fix this, but it's not a major problem ATM.
        included_content = read_file(filename)
        
        # Include it into the return string
        ret = ret.replace(include, included_content)
        
    return ret

if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) != 3:
        print("\nSyntax:\ntinySSG.py inputfile outputfile\n")
        raise SystemExit
    
    raw = read_file(sys.argv[1])
    processed = add_includes(raw)
    
    # TODO: write processed to new file
