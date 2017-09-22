#!/usr/bin/env python
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("search_path", help="The root search path")
parser.add_argument("text_path", help="a path to an text file, which will be appended to regex found files")
parser.add_argument("regex_expresion", help="The regex expresion based on which file search is made starting from --search_path")
parser.add_argument("--del_lines", help="Optional argument to delete the first specifiec lines from the found txt", type=int)
args = parser.parse_args()

if not os.path.exists(args.search_path):
    print ("The root search path is not valid, please add a valid search path")
    exit()
if not os.path.isfile(args.text_path):
    print ("The path to the text file is not valid, please add a valid text path")
    exit()
try:
    pattern = re.compile(args.regex_expresion)
except re.error:
    print("The entered regex is not a valid regex, please enter another regex")
    exit()

template_txt = open(args.text_path, "r")
template_content = template_txt.read()
for root, dirs, files in os.walk(args.search_path):
    for name in files:
        for match in re.finditer(pattern, name):
            print(os.path.join(root, name))
            found_txt = open(os.path.join(root, name), "r+")
            found_content = found_txt.read()
            found_txt.seek(0,0)
            found_txt.truncate()
            if not args.del_lines:
                found_txt.write(template_content + found_content)
            else:
                found_txt.write(template_content + '\n'.join(found_content.split('\n')[args.del_lines:]))    
            found_txt.close()
template_txt.close()
