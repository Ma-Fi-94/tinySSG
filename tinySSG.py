# -*- coding: utf-8 -*-

import configparser
import frontmatter
import glob
import markdown
import os
import re
import shutil
import sys
import time
import typing

def md_to_html(md: str) -> str:
	'''Convert a MD string to HTML'''
	try:
		return markdown.markdown(md)
	except:
		print("[X] Error convertig markdown file to HTML. Aborting.", file=sys.stderr)
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
		print("[X] Error making clean output folder. Aborting.", file=sys.stderr)
		raise SystemExit


def read_record(filepath: str) -> (dict, str):
	'''Extract header and contents from a page record'''
	try:
		with open(filepath) as f:
			record = frontmatter.load(filepath)
	except:
		print("[X] Error loading input file >>>" + filepath + "<<<. Aborting.", file=sys.stderr)
		raise SystemExit
	
	return (record.metadata, record.content)


def read_template(filepath: str) -> str:
	try:
		with open(filepath, "r") as f:
			template = f.read()
	except:
		print("[X] Error loading template file >>>" + filepath + "<<<. Aborting.", file=sys.stderr)
		raise SystemExit
	
	assert len(template) > 0, "[X] Template file >>>" + filepath + "<<< has zero length. Aborting."
	
	return template


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
			print ("[X] Could not find tag " + tag + " in metadata dictionary. Aborting.", file=sys.stderr)
			raise SystemExit
	
	return page


def construct_destination_filename(filename: str, path_output: str) -> str:
		basename = os.path.basename(filename)
		basename_wout_ext = os.path.splitext(basename)[0]
		if path_output[-1] == "/":
			path_output = path_output[:-1]
		destination = path_output + "/" + basename_wout_ext + ".html"
		return destination
		

def write_page(destination: str, page: str) -> None:
	try:
		with open(destination, "w") as f:
			f.write(page)
	except:
		print("[X] Error writing to file " + destination + ". Aborting.", file=sys.stderr)
		raise SystemExit

def load_config(config_file: str) -> (str, str, str, bool):
	try:
		config = configparser.ConfigParser()
		config.read(config_file)
	except:
		print ("[X] Could not read configuration file " + config_file + ". Aborting.", file=sys.stderr)
		raise SystemExit
	
	assert "CONFIG" in config.sections(), "No [CONFIG] section in configuration file " + config_file + ". Aborting."
	
	try:
		path_rawfiles = config["CONFIG"]["path_rawfiles"]
		path_output = config["CONFIG"]["path_output"]
		template_file = config["CONFIG"]["template_file"]
		verbose = config.getboolean("CONFIG", "verbose")
	except:
		print ("[X] Could not parse configuration file " + config_file + ". Please provide keys path_rawfiles, path_output, template_file, verbose. Aborting.", file=sys.stderr)
		raise SystemExit
	
	assert len(path_rawfiles) > 0, "[X] path_rawfiles is of zero length in configuration file. Aborting."
	assert len(path_output) > 0, "[X] path_output is of zero length in configuration file. Aborting."
	assert len(template_file) > 0, "[X] template_file is of zero length in configuration file. Aborting."

	return path_rawfiles, path_output, template_file, verbose
	
	
def main() -> None:
	config_file = "./tinySSG.ini"
	path_rawfiles, path_output, template_file, verbose = load_config(config_file)
	if verbose:
		print ("[*] Loaded configuration file " + config_file + ".")
		print ("\t[*] path_rawfiles: " + path_rawfiles)
		print ("\t[*] path_output: " + path_output)
		print ("\t[*] template_file: " + template_file)
		print ("\t[*] tverbose: " + str(verbose))

	starttime_millisec = time.time()*1000
	
	# Make empty output folder and read template file
	make_output_folder(path_output)
	if verbose: print("[*] Made output folder.")
	template = read_template(template_file)
	if verbose: print("[*] Read template file.")
	
	# Process the indidividual MD files
	for filename in glob.iglob(path_rawfiles+"/*.md"):
		# Read current MD file
		metadata, content_md = read_record(filename)
		
		# Generate HTML from MD file
		page = generate_site(template, metadata, content_md)
			
		# Write HTML file to HDD
		destination = construct_destination_filename(filename, path_output)
		write_page(destination, page)
		
		if verbose: print("[*] Processed " + filename + " to " + destination + ".")
	
	
	endtime_millisec = time.time()*1000
	print("[*] Finished in " + str(round(endtime_millisec-starttime_millisec,2)) + " ms.")

if __name__ == "__main__":
	main()
