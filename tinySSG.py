# -*- coding: utf-8 -*-

import configparser
import glob
import markdown
import os
import re
import shutil
import sys
import time

import typing
from typing import Tuple

import log

logger = log.Logger()


def abort(message: str) -> None:
    logger.critical(message)
    raise SystemExit


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


def read_file(filepath: str) -> str:
    '''Generic file reading function'''
    try:
        with open(filepath, "r") as f:
            filecontents = f.read()
    except:
        abort("Error loading file >>>" + filepath + "<<<. Aborting.")
    if len(filecontents) == 0:
        abort("File >>>" + filepath + "<<< has zero length. Aborting.")
    return filecontents


def write_file(destination: str, contents: str) -> None:
    '''Generic file writing function'''
    try:
        with open(destination, "w") as f:
            f.write(contents)
    except:
        abort("Error writing to file " + destination + ". Aborting.")


def generate_site(template: str, content: str) -> str:
    '''Compose the HTML file from the template and the input HTML'''
    page = template[:]

    # Convert page content from MD to HTML and add it to the template
    if not "{{.content}}" in page:
        abort("No {{.content}} tag found. Aborting.")
    page = page.replace("{{.content}}", content)

    return page


def construct_destination_filename(filename: str, path_output: str) -> str:
    basename = os.path.basename(filename)
    basename_wout_ext = os.path.splitext(basename)[0]
    if path_output[-1] == "/":
        path_output = path_output[:-1]
    destination = path_output + "/" + basename_wout_ext + ".html"
    return destination


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


def process_input_files(path_rawfiles: str, template: str,
                        path_output: str) -> None:
    for filename in glob.iglob(path_rawfiles + "/*.html"):
        # Read current HTML file
        content = read_file(filename)

        # Generate HTML from MD file
        page = generate_site(template, content)

        # Write HTML file to HDD
        destination = construct_destination_filename(filename, path_output)
        write_file(destination, page)

        logger.info_verbose("Processed " + filename + " to " + destination +
                            ".")


def main() -> None:  # pragma: no cover
    config_file = "./tinySSG.ini"
    path_rawfiles, path_output, template_file, verbose = load_config(
        config_file)

    logger.set_verbose(verbose)
    logger.info_verbose("Loaded configuration file " + config_file + ".")
    logger.info_verbose("\tpath_rawfiles: " + path_rawfiles)
    logger.info_verbose("\tpath_output: " + path_output)
    logger.info_verbose("\ttemplate_file: " + template_file)
    logger.info_verbose("\tverbose: " + str(verbose))

    starttime_millisec = time.time() * 1000

    make_output_folder(path_output)
    logger.info_verbose("Made output folder " + path_output + ".")

    template = read_file(template_file)
    logger.info_verbose("Read template file " + template_file + ".")

    process_input_files(path_rawfiles, template, path_output)
    logger.info_verbose("Processed all input files.")

    endtime_millisec = time.time() * 1000
    logger.info("Finished in " +
                str(round(endtime_millisec - starttime_millisec, 2)) + " ms.")


if __name__ == "__main__":  # pragma: no cover
    main()
