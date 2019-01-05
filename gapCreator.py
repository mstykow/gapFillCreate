#! python3
# Program creates a gap in a sequence of filenames with a characteristic prefix
# so new files can be added.

import re, os, shutil

# Define regex patterns needed in program.
digitsRegex = re.compile(r'([1-9]+|[1-9]+\d+)$')
lengthRegex = re.compile(r'\d+$')

# Function to prefix an integer with as many zeros as needed to fit the pattern.
def digify(num, nomLength):
    stringNum = str(num)
    actLength = len(stringNum)
    for i in range(nomLength - actLength):
        stringNum = '0' + stringNum
    return stringNum

# Function to determine the length of an integer pattern within a filename, e.g.,
# test00312.txt has length 5.
def indexLength(file):
    mo = lengthRegex.search(os.path.splitext(file)[0])
    return len(mo.group())

# Create list of files in the cwd to be renamed sequentially and determine the integer pattern length.
prefix = input("Enter your files' prefix: ")
allFiles = os.listdir(os.getcwd())
prefixFiles = []

for file in allFiles:
    if file.startswith(prefix):
        prefixFiles.append(file)

length = indexLength(prefixFiles[0])

gapIndex = int(input('Insert a file after the file ending in the number: '))

# Rename files after user-specified index counting down from last file.
for i in range(len(prefixFiles) - 1, -1, -1):
    mo = digitsRegex.search(os.path.splitext(prefixFiles[i])[0])
    if int(mo.group()) <= gapIndex:
        continue
    shutil.move(prefixFiles[i], prefix + digify(int(mo.group()) + 1, length) + os.path.splitext(prefixFiles[i])[1])
