import glob, re, sys, pathlib

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


def get_input_filenames(inputfolder: str, inputfile_extension: str) -> [str]:
    return list(glob.iglob(inputfolder + "/*." + inputfile_extension))


def replace_extensions(filenames: [str], old_extension: str, new_extension: str) -> [str]:
    return [s[:-len(old_extension)]+new_extension for s in filenames]


if __name__ == "__main__":  # pragma: no cover
    # python3 tinySSG.py --file inputfile outputfile
    # python3 tinySSG.py --folger path/to/folder inputextension outputextension
    
    if len(sys.argv) == 4 and sys.argv[1] == "--file":
        # Setting up single-file mode
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]

        # Load and process input file; write to HDD.
        print(input_filename, " --> ", output_filename)
        raw = read_file(input_filename)
        processed = add_includes(raw)
        write_file(output_filename, processed)

    elif len(sys.argv) == 5 and sys.argv[1] == "--folder":
        # Setting up whole-folder mode
        inputfolder = sys.argv[2]
        inputfile_extension = sys.argv[3]
        outputfile_extension = sys.argv[4]
        
        # Some sanitising
        if inputfile_extension == outputfile_extension:
            abort("Input file extension must be different from output file extension.")
        if inputfile_extension[0] == ".":
            inputfile_extension = inputfile_extension[1:]
        if outputfile_extension[0] == ".":
            outputfile_extension = outputfile_extension[1:]
        
        
        # Get all files from inputfolder which have the inputfile_extension
        input_filenames = get_input_filenames(inputfolder, inputfile_extension)
    
        # Generate the corresponding outputfile names
        output_filenames = replace_extensions(input_filenames, inputfile_extension, outputfile_extension)
    
        # Process them one after another and write them to HDD
        for input_filename, output_filename in zip(input_filenames, output_filenames):
            print(input_filename, " --> ", output_filename)
            raw = read_file(input_filename)
            processed = add_includes(raw)
            write_file(output_filename, processed)
            
    else:
        syntax = "\nSyntax:\n" + \
        "tinySSG.py --file inputfile outputfile\n" + \
        "tinySSG.py --folder path/to/folder inputextension outputextension\n"
        abort(syntax)
    
    
