#! python3
# Program finds gaps in a sequence of filenames with a characteristic prefix and closes these
# gaps by renaming the files.

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

# Function to fill gaps by renaming only those files that need it.
# Note: It would have been much easier to just immediately rename all files sequentially but in
# the interest of the programming exercise the program was made more selective.
def gapFiller(fileList, num):
    for i in range(len(fileList)):
        mo = digitsRegex.search(os.path.splitext(fileList[i])[0])
        if int(mo.group()) == (i + 1):
            continue
        shutil.move(fileList[i], prefix + digify(i+1, num) + os.path.splitext(fileList[i])[1])

# Function to rename files up to user-specified index counting down from last file.
def gapCreator(fileList, num1, num2):
    for i in range(len(fileList) - 1, -1, -1):
        mo = digitsRegex.search(os.path.splitext(fileList[i])[0])
        if int(mo.group()) <= num2:
            continue
        shutil.move(fileList[i], prefix + digify(int(mo.group()) + 1, num1) + os.path.splitext(fileList[i])[1])

# Create list of files in the cwd to be renamed sequentially and determine the integer pattern length.
prefix = input("Enter your files' prefix: ")
allFiles = os.listdir(os.getcwd())
prefixFiles = []

for file in allFiles:
    if file.startswith(prefix):
        prefixFiles.append(file)

length = indexLength(prefixFiles[0])

# Call correct function depending on user's needs.
option = ''
while option != 'fill' and option != 'create':
    option = input('Would you like to "fill" or "create" a gap? ')
    if option == 'fill':
        gapFiller(prefixFiles, length)
    elif option == 'create':
        gapIndex = int(input('Insert a file after the file ending in the number: '))
        gapCreator(prefixFiles, length, gapIndex)
