# -*- coding: utf-8 -*-

import configparser
import frontmatter  # type: ignore
import glob
import markdown
import os
import re
import shutil
import sys
import time
import typing
from typing import Tuple


def abort(message: str) -> None:
    print("[X] " + message, file=sys.stderr)
    raise SystemExit


def info(message: str, verbose: bool) -> None:
    if verbose:
        print("[*] " + message)


def md_to_html(md: str) -> str:
    '''Convert a MD string to HTML'''
    try:
        ret = markdown.markdown(md)
    except:
        abort("Error convertig markdown file to HTML. Aborting.")

    return ret


def make_output_folder(path: str) -> None:
    '''Generate an empty output folder for the generated HTML files'''
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            shutil.rmtree(path)
            os.mkdir(path)
    except:
        abort("Error making clean output folder. Aborting.")


def read_record(filepath: str) -> Tuple[dict, str]:
    '''Extract header and contents from a page record'''
    try:
        with open(filepath) as f:
            record = frontmatter.load(filepath)
    except:
        abort("Error loading input file >>>" + filepath + "<<<. Aborting.")

    return (record.metadata, record.content)


def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            filecontents = f.read()
    except:
        abort("Error loading file >>>" + filepath + "<<<. Aborting.")

    if len(filecontents) == 0:
        abort("File >>>" + filepath + "<<< has zero length. Aborting.")

    return filecontents


def generate_site(template: str, metadata: dict, content_md: str) -> str:
    '''Compose the HTML file from the template HTML, the metadata dict, and the content in MD format.'''
    page = template[:]

    # Convert page content from MD to HTML and add it to the template
    content = md_to_html(content_md)
    page = page.replace("{{.content}}", content)

    # Now, we need to find and replace all tags
    tags = re.findall(r"{{\..+?}}", page)
    for tag in tags:
        try:
            page = page.replace(tag, metadata[tag[3:-2]])
        except:
            abort(" Could not find tag " + tag +
                  " in metadata dictionary. Aborting.")

    return page


def construct_destination_filename(filename: str, path_output: str) -> str:
    basename = os.path.basename(filename)
    basename_wout_ext = os.path.splitext(basename)[0]
    if path_output[-1] == "/":
        path_output = path_output[:-1]
    destination = path_output + "/" + basename_wout_ext + ".html"
    return destination


def write_file(destination: str, contents: str) -> None:
    try:
        with open(destination, "w") as f:
            f.write(contents)
    except:
        abort("Error writing to file " + destination + ". Aborting.")


def load_config(config_file: str) -> Tuple[str, str, str, bool]:
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
    except:
        abort("Could not read configuration file " + config_file +
              ". Aborting.")

    if not "CONFIG" in config.sections():
        abort("No [CONFIG] section in configuration file " + config_file +
              ". Aborting.")

    try:
        path_rawfiles = config["CONFIG"]["path_rawfiles"]
        path_output = config["CONFIG"]["path_output"]
        template_file = config["CONFIG"]["template_file"]
        verbose = config.getboolean("CONFIG", "verbose")
    except:
        abort(
            "Could not parse configuration file " + config_file +
            ". Please provide keys path_rawfiles, path_output, template_file, verbose. Aborting."
        )

    if len(path_rawfiles) == 0:
        abort(
            "path_rawfiles is of zero length in configuration file. Aborting.")
    if len(path_output) == 0:
        abort("path_output is of zero length in configuration file. Aborting.")
    if len(template_file) == 0:
        abort(
            "template_file is of zero length in configuration file. Aborting.")

    return path_rawfiles, path_output, template_file, verbose


def main() -> None:
    config_file = "./tinySSG.ini"
    path_rawfiles, path_output, template_file, verbose = load_config(
        config_file)
    info("Loaded configuration file " + config_file + ".", verbose)
    info("\tpath_rawfiles: " + path_rawfiles, verbose)
    info("\tpath_output: " + path_output, verbose)
    info("\ttemplate_file: " + template_file, verbose)
    info("\tverbose: " + str(verbose), verbose)

    starttime_millisec = time.time() * 1000

    # Make empty output folder and read template file
    make_output_folder(path_output)
    info("Made output folder.", verbose)
    template = read_file(template_file)
    info("Read template file.", verbose)

    # Process the indidividual MD files
    for filename in glob.iglob(path_rawfiles + "/*.md"):
        # Read current MD file
        metadata, content_md = read_record(filename)

        # Generate HTML from MD file
        page = generate_site(template, metadata, content_md)

        # Write HTML file to HDD
        destination = construct_destination_filename(filename, path_output)
        write_file(destination, page)

        info("Processed " + filename + " to " + destination + ".", verbose)

    endtime_millisec = time.time() * 1000
    print("[*] Finished in " +
          str(round(endtime_millisec - starttime_millisec, 2)) + " ms.")


if __name__ == "__main__":
    main()
