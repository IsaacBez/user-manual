import os, subprocess, yaml

import os.path
from os import path

# Function to write YAML value
def writeto(file, id, value):
    str_list = value.split("\n")
    file.write(id)
    file.write(": ")

    if len(str_list) == 1:
        file.write(value)
        file.write("\n")
        return
    
    file.write("|\n")
    for mystr in str_list:
        file.write("  ")
        file.write(mystr)
        file.write("\n")

# Get eletra options
with open("_metadata.yaml", "r") as stream:
    try:
        eletra_options = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Get PDF options and PANDOC options
with open(eletra_options['eletra-options-file'], "r") as options_stream:
    try:
        options_map = yaml.safe_load(options_stream)
        pdf_options = options_map["pdf-options"]
        pandoc_options = options_map["pandoc-options"]
    except yaml.YAMLError as exc:
        print(exc)

# Get output path
output_file = eletra_options["eletra-out-pdf"]

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

# Get input files
input_files = eletra_options["eletra-files"]
files = '___tmp_metadata.yaml'
for file in input_files:
     files = files + ' ' + file

# Write tmp metadata with pandoc and eletra options in a single file
with open("___tmp_metadata.yaml", "w") as tmp_metada:
    tmp_metada.write("---\n")
        
    for key in pandoc_options:
        writeto(tmp_metada, key, str(pandoc_options[key]))

    for key in eletra_options:
        writeto(tmp_metada, key, str(eletra_options[key]))
    
    tmp_metada.write("...")

# Execute the command
command = 'pandoc '+pdf_options+' '+files+' -o '+output_file
print(command)
exit_code = subprocess.call(command)

# Remove temporary metadata file
os.remove("___tmp_metadata.yaml")

# Exit
os._exit(exit_code)
