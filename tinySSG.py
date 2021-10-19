# -*- coding: utf-8 -*-

import frontmatter
import glob
import markdown
import os
import re
import shutil
import time
import typing

def md_to_html(md: str) -> str:
	'''Convert a MD string to HTML'''
	try:
		return markdown.markdown(md)
	except:
		print("[X] Error convertig markdown file to HTML. Aborting.")
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
		print("[X] Error making clean output folder. Aborting.")
		raise SystemExit


def read_record(filepath: str) -> (dict, str):
	'''Extract header and contents from a page record'''
	try:
		with open(filepath) as f:
			record = frontmatter.load(filepath)
	except:
		print("[X] Error loading input file >>>" + filepath + "<<<. Aborting.")
		raise SystemExit
	
	return (record.metadata, record.content)


def read_template(filepath: str) -> str:
	try:
		with open(filepath, "r") as f:
			template = f.read()
	except:
		print("[X] Error loading template file >>>" + filepath + "<<<. Aborting.")
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
			print ("[X] Could not find tag " + tag + " in metadata dictionary. Aborting.")
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
		print("[X] Error writing to file " + destination + ". Aborting.")
		raise SystemExit


def main() -> None:
	# Configuration
	path_rawfiles = "./raw"
	path_output = "./public_html/"
	template_file = "./template.html"
	
	starttime_millisec = time.time()*1000
	
	# Make empty output folder and read template file
	make_output_folder(path_output)
	print("[*] Made output folder.")
	template = read_template(template_file)
	print("[*] Read template file.")
	
	# Process the indidividual MD files
	for filename in glob.iglob(path_rawfiles+"/*.md"):
		# Read current MD file
		metadata, content_md = read_record(filename)
		
		# Generate HTML from MD file
		page = generate_site(template, metadata, content_md)
			
		# Write HTML file to HDD
		destination = construct_destination_filename(filename, path_output)
		write_page(destination, page)
		
		print("[*] Processed " + filename + " to " + destination + ".")
	
	
	endtime_millisec = time.time()*1000
	print("[*] Finished in " + str(round(endtime_millisec-starttime_millisec,2)) + " ms.")

if __name__ == "__main__":
	main()
