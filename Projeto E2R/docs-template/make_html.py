import os, subprocess, yaml

import os.path
from os import path

with open("_metadata.yaml", "r") as stream:
    try:
        eletra_options = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(eletra_options['eletra-options-file'], "r") as options_stream:
    try:
        options_map = yaml.safe_load(options_stream)
        html_options = options_map["html-options"]
    except yaml.YAMLError as exc:
        print(exc)

# Get Title
title = eletra_options["subtitle"]

# Get Options
options = html_options + ' --metadata title=\"' + title + "\""

# Get output path
output_file = eletra_options["eletra-out-html"]

# Prepare output path
head_output_file, tail_output_file = os.path.split(output_file)
if head_output_file.strip()!="":
    if not path.isdir(head_output_file):
        try:
            os.mkdir(head_output_file)
        except OSError:
            print ("Creation of the directory [%s] failed" % head_output_file)
        else:
            print ("Successfully created the directory [%s] " % head_output_file)
    else:
        print ("The directory [%s] already exists" % head_output_file) 

# Get Input Files
input_files = eletra_options["eletra-files"]
files = ''
for file in input_files:
    files = files + ' ' + file

# Execute the command
command = 'pandoc '+files+' -o '+output_file+' '+options
print(command)
exit_code = subprocess.call(command)

# Exit
os._exit(exit_code)
