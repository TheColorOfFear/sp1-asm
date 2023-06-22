print("\033c")
print("SP1 ASSEMBLER || (C)2023  723179\n")
# get input and choose output filename
with open(input("File input name? "), "r", encoding="utf-8") as f:
    file = f.read()
    fileIn = file.splitlines()
    length = len(str(len(file))) + 1
outName = input("File output name? ")

## Variables
currentPos = 0
# jump point lists
jpName = []
jpPos = []

#loop through once to find where jump points are
for i in range(len(fileIn)):
    if fileIn[i][0] == "j":
        jpName.append(fileIn[i][1:])
        jpPos.append(currentPos + 1)
        print("JP: " + fileIn[i][1:] + " :" + str(currentPos + 1))
    else:
        if fileIn[i][0] == "=" or fileIn[i][0] == "g":
            currentPos += 8
        else:
            currentPos += len(fileIn[i])

output = ""

for i in range(len(fileIn)):
    if fileIn[i][0] == "j":
        pass
    elif fileIn[i][0] == "g":
        output += "0604"
        tempOut = str(jpPos[jpName.index(fileIn[i][1:])])
        while len(tempOut) < 4:
            tempOut = "0" + tempOut
        output += tempOut
    elif fileIn[i][0] == "=":
        output += "2004"
        tempOut = str(jpPos[jpName.index(fileIn[i][1:])])
        while len(tempOut) < 4:
            tempOut = "0" + tempOut
        output += tempOut
    else:
        output += fileIn[i]

if outName == "":
    print(output)
else:
    with open(outName, "w", encoding="utf-8") as o:
        o.write(output)
