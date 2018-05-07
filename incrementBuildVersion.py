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
args = parser.parse_args()
if args.enable:
    print ("Incrementing Build version")
else:
    print ("Incrementual building is deactivated") 
    exit()

resourceFileName = "InfoSrvService.rc"
resourceFilePath = os.path.join(os.path.dirname(__file__), resourceFileName)

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