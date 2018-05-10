#!/usr/bin/env python3
import os
import re
import fileinput
import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("--enable", type=str2bool, nargs='?',
                        const=True, default="False",
                        help="Enable/Disable incrementBuild mode.")
parser.add_argument("--resource_path", help="The path to the .rc file, in order to modify it")                        
args = parser.parse_args()

if args.enable:
    if args.resource_path is None:
        parser.error("--resoarce_path not provided, when enable is set to true, --resource_path should be provided")
        exit()
    print ("Incrementing Build version")
else:
    print ("Incrementual building is deactivated") 
    exit()
if not os.path.isfile(args.resource_path):
    print ("The root search path is not valid, please add a valid search path")
    exit()

resourceFilePath = args.resource_path

for line in fileinput.FileInput(resourceFilePath, inplace=False):
    if "FILEVERSION" in line: 
        print("found FILEVERSION")
        fileVersion = re.findall(r"[\d+']+|[.!?;]",line)
        print (fileVersion)
    if "PRODUCTVERSION" in line: 
        print("found PRODUCTVERSION")
        productVersion = re.findall(r"[\d+']+|[.!?;]",line)
        print (productVersion)
# We construct two lists productVersion and fileVersion, in wich we have the version extracted from the file

FileVersionToSearch             = ','.join(str(x) for x in fileVersion)
FileVersionToSearchWithSpace    = ', '.join(str(x) for x in fileVersion)
ProductVersionToSearch          = ','.join(str(x) for x in productVersion)
ProductVersionToSearchWithSpace = ', '.join(str(x) for x in productVersion)
# We construct two strings to search in a line for it (one with space and one without) in order to easily replace with the incremented version
print ("FileVersionToSearch = ", FileVersionToSearch)
print ("FileVersionToSearchWithSpace = ", FileVersionToSearchWithSpace)
print ("ProductVersionToSearch = ", ProductVersionToSearch)
print ("ProductVersionToSearchWithSpace = ", ProductVersionToSearchWithSpace)
# we increment the last element of the list (that's what the incremental build should do)
fileVersion[-1] = int(fileVersion[-1]) + 1
productVersion[-1] = int(productVersion[-1]) + 1
FileVersionToReplace             = ','.join(str(x) for x in fileVersion)
FileVersionToReplaceWithSpace    = ', '.join(str(x) for x in fileVersion)
ProductVersionToReplace          = ','.join(str(x) for x in productVersion)
ProductVersionToReplaceWithSpace = ', '.join(str(x) for x in productVersion)
#We construct two string with the incremented versions, and we will use them for replacement.
print ("FileVersionToReplace = ", FileVersionToReplace)
print ("FileVersionToReplaceWithSpace = ", FileVersionToReplaceWithSpace)
print ("ProductVersionToReplace = ", ProductVersionToReplace)
print ("ProductVersionToReplaceWithSpace = ", ProductVersionToReplaceWithSpace)


for line in fileinput.FileInput(resourceFilePath, inplace=True):
    if   "FILEVERSION" in line: 
        print(line.replace(FileVersionToSearch, FileVersionToReplace), end='')
    elif "FileVersion" in line: 
        print(line.replace(FileVersionToSearchWithSpace, FileVersionToReplaceWithSpace), end='')
    elif "PRODUCTVERSION" in line:
        print(line.replace(ProductVersionToSearch, ProductVersionToReplace), end='') 
    elif "ProductVersion" in line:
        print(line.replace(ProductVersionToSearchWithSpace, ProductVersionToReplaceWithSpace), end='')
    else:
        print(line, end='')

print("Python script succefully exited without Errors")    