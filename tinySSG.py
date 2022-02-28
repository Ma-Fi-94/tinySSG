import glob, re, sys, pathlib
from typing import List, Optional


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


def add_includes(raw: str, path: Optional[str]) -> str:
    # Local copy to operate on
    ret = str(raw)

    # The pattern indicating a file include
    # We need to use parentheses to denote the matched group nb. 1
    include_pattern = r"^#include (.+)$"

    # Substitute all occurences at once with re.sub() and a substitution function
    # FIXME: Reading from file adds a newline at the end by default
    # FIXME: We might want to fix this, but it's not a major problem ATM.
    if path is not None:
        f = lambda match_obj: read_file(path + "/" + match_obj.group(1))
    else:
        f = lambda match_obj: read_file(match_obj.group(1))
    ret = re.sub(include_pattern, f, ret, flags=re.MULTILINE)

    return ret


def replace_defines(raw: str) -> str:
    # Local copy to operate on
    ret = str(raw)

    # The pattern indicating a definition of a variable
    # We use parentheses to denote the two matched groups
    define_pattern = '^#globaldefine (.+) (".+")$'

    # Find all replacements (variable -> contents)
    replacements = re.findall(define_pattern, ret, flags=re.MULTILINE)

    # Now we can delete all lines with #define statements from the input
    # FIXME: Currently, this leaves newlines
    # FIXME: We might want to fix it, but it's not urgent.
    ret = re.sub(define_pattern, '', ret, flags=re.MULTILINE)

    # And now, we just perform the replacements and are done.
    for old, new in replacements:
        new_stripped = new[1:-1]  # strip of enclosing quotation marks
        ret = re.sub(old, new_stripped, ret, flags=re.MULTILINE)

    return ret


def process_file(inputfolder: Optional[str], input_filename: str,
                 output_filename: str):
    '''Read and process inputfile, write to outputfile'''
    print(input_filename, " --> ", output_filename)
    raw = read_file(input_filename)
    raw_with_includes = add_includes(raw=raw, path=inputfolder)
    processed = replace_defines(raw_with_includes)
    write_file(output_filename, processed)
    print("done.")


def get_filenames_by_extension(folder: str, extension: str) -> List[str]:
    '''Return a list of file names in specified folder which have the desired extension'''
    return glob.glob(folder + "/*." + extension)


def replace_extension(filename: str, old_extension: str,
                      new_extension: str) -> str:
    '''Replace the extension of a filename'''
    return filename[:-len(old_extension)] + new_extension


if __name__ == "__main__":  # pragma: no cover

    # Single-file mode
    if len(sys.argv) == 4 and sys.argv[1] == "--file":
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
        process_file(inputfolder=None,
                     input_filename=input_filename,
                     output_filename=output_filename)

    # Whole-folder mode
    elif len(sys.argv) == 5 and sys.argv[1] == "--folder":
        # Setup
        inputfolder = sys.argv[2]
        inputfile_extension = sys.argv[3]
        outputfile_extension = sys.argv[4]

        # Some sanitising
        if inputfile_extension == outputfile_extension:
            abort(
                "Input file extension must be different from output file extension."
            )
        if inputfile_extension[0] == ".":
            inputfile_extension = inputfile_extension[1:]
        if outputfile_extension[0] == ".":
            outputfile_extension = outputfile_extension[1:]

        # Get all files from inputfolder which have the inputfile_extension
        input_filenames = get_filenames_by_extension(inputfolder,
                                                     inputfile_extension)

        # And process them
        for input_filename in input_filenames:
            output_filename = replace_extension(input_filename,
                                                inputfile_extension,
                                                outputfile_extension)
            process_file(inputfolder=inputfolder,
                         input_filename=input_filename,
                         output_filename=output_filename)

# Recursive mode
    elif len(sys.argv) == 5 and sys.argv[1] == "--recursive":
        # Setup
        inputfolder = sys.argv[2]
        inputfile_extension = sys.argv[3]
        outputfile_extension = sys.argv[4]

        # Some sanitising
        if inputfile_extension == outputfile_extension:
            abort(
                "Input file extension must be different from output file extension."
            )
        if inputfile_extension[0] == ".":
            inputfile_extension = inputfile_extension[1:]
        if outputfile_extension[0] == ".":
            outputfile_extension = outputfile_extension[1:]

        # Get all input files in the folder, as well as all of its subfolders
        # TODO

        # And process them
        # TODO

        raise NotImplementedError

    else:
        syntax = "\nSyntax:\n" + \
        "tinySSG.py --file inputfile outputfile\n" + \
        "tinySSG.py --folder path/to/folder inputextension outputextension\n" + \
        "tinySSG.py --recursive path/to/folder inputextension outputextension\n"
        abort(syntax)
