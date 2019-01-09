#! python3
# Program finds gaps in a sequence of filenames with a characteristic prefix and closes these
# gaps by renaming the files.

import re, os, shutil

# Define regex patterns needed in program.
numRegex = re.compile(r'([1-9]+|[1-9]+\d+)$')
fullNumRegex = re.compile(r'\d+$')

# Function to prefix an integer with as many zeros as needed to fit a pattern.
def digify(num, nomLength):
    stringNum = str(num)
    actLength = len(stringNum)
    for i in range(nomLength - actLength):
        stringNum = '0' + stringNum
    return stringNum

# Function to fill gaps by renaming only those files that need it.
# Note: It would have been much easier to just immediately rename all files sequentially but in
# the interest of the programming exercise the program was made more selective.
def gap_filler(fileList):
    for i in range(len(fileList)):
        filename = os.path.splitext(fileList[i])[0]
        mo1 = fullNumRegex.search(filename)
        fullNumLength = len(mo1.group())
        mo2 = numRegex.search(filename)
        indexNum = int(mo2.group())
        extension = os.path.splitext(fileList[i])[1]
        if indexNum == (i + 1):
            continue
        shutil.move(fileList[i], fullNumRegex.sub(digify(i+1, fullNumLength), filename) + extension)

# Function to rename files after user-specified index counting down from last file.
def gap_creator(fileList, gapPosition):
    for i in range(len(fileList) - 1, -1, -1):
        filename = os.path.splitext(fileList[i])[0]
        mo1 = fullNumRegex.search(filename)
        fullNumLength = len(mo1.group())
        mo2 = numRegex.search(filename)
        indexNum = int(mo2.group())
        extension = os.path.splitext(fileList[i])[1]
        if indexNum <= gapPosition:
            continue
        shutil.move(fileList[i], fullNumRegex.sub(digify(indexNum + 1, fullNumLength), filename) + extension)

# Create list of files in the cwd to be renamed sequentially and determine the integer pattern length.
prefix = input("Enter your files' prefix: ")
allFiles = os.listdir(os.getcwd())
prefixFiles = []

for file in allFiles:
    if file.startswith(prefix):
        prefixFiles.append(file)

# Call correct function depending on user's needs.
option = ''
while option != 'fill' and option != 'create':
    option = input('Would you like to "fill" or "create" a gap? ')
    if option == 'fill':
        gap_filler(prefixFiles)
    elif option == 'create':
        gapIndex = int(input('Create a gap after the file ending in the number: '))
        gap_creator(prefixFiles, gapIndex)
