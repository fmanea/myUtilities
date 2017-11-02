#!/usr/bin/env python3
import argparse
import os
import re
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument("root_path", help="The root search path")
parser.add_argument("regex_expresion", help="The regex expresion based on which file search is made starting from --search_path")
parser.add_argument("text_to_search", help="The text that needs to be searched and replaced")
parser.add_argument("text_to_replace", help="The text to replace with")
args = parser.parse_args()

if not os.path.exists(args.root_path):
    print ("The root search path is not valid, please add a valid search path")
    exit()
try:
    pattern = re.compile(args.regex_expresion)
except re.error:
    print("The entered regex is not a valid regex, please enter another regex")
    exit()

textToSearch = args.text_to_search
textToReplace = args.text_to_replace
print ("Text to search for: ", textToSearch)
print ("Text to replace it with: ", textToReplace)


for root, dirs, files in os.walk(args.root_path):
    for name in files:
        for match in re.finditer(pattern, name):
            print('Processing file (matched by regex): ', os.path.join(root, name))
            for line in fileinput.FileInput( os.path.join(root, name), inplace=True):
                print(line.replace(textToSearch, textToReplace), end='')
