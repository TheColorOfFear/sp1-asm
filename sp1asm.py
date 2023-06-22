print("\033c")
print("SP1 ASSEMBLER || (C)2023  723179\n")

def lenHex(funcLength):
    funcOutput = hex(funcLength)[2:]
    while len(funcOutput) < 2:
        funcOutput = "0" + funcOutput
    return funcOutput

#define some default variables
##does it print the location of every jump point?
jpPrint = False

# get input and choose output filename
with open(input("File input name? "), "r", encoding="utf-8") as f:
    file = f.read()
    fileIn = file.splitlines()
    length = len(str(len(file))) + 1
outName = input("File output name? ")

while 1 == 1:
    arg = input("Extra Arguments? ")
    if arg == "":
        break
    if arg[0] in ["l","j"]:
        #if the automatic get-length thing breaks the program, here's an option to fix it preemptively
        if arg[0] == "l":
            length = int(arg[1:])
        elif arg[0] == "j":
            if arg[1] == "0":
                jpPrint = False
            else:
                jpPrint = True
    else:
        print("Syntax Error")

## Variables
currentPos = 0
# jump point lists
jpName = []
jpPos = []

#loop through once to find where jump points are
for i in range(len(fileIn)):
    item = fileIn[i].lstrip()
    if len(item) > 0:
        if item[0] == "j":
            jpName.append(item[1:])
            jpPos.append(currentPos + 1)
            if jpPrint:
                print("JP: " + item[1:] + " :" + str(currentPos + 1))
        else:
            if item[0] in ["=", "g", ">", "<"]:
                currentPos += (4 + length)
            else:
                currentPos += len(item)

output = ""

for i in range(len(fileIn)):
    item = fileIn[i].lstrip()
    if len(item) > 0:
        if item[0] == "j":
            pass
        elif item[0] in ["=","g", ">", "<"]:
            if item[0] == "g":
                output += "06"
            elif item[0] == "=":
                output += "20"
            elif item[0] == ">":
                output += "21"
            elif item[0] == "<":
                output += "22"
            output += lenHex(length)
            tempOut = str(jpPos[jpName.index(item[1:])])
            while len(tempOut) < length:
                tempOut = "0" + tempOut
            output += tempOut
        elif item[2:4] == "##":
            output += item[0:2]
            output += lenHex(len(item[4:]))
            output += item[4:]
        else:
            output += item

if outName == "":
    print(output)
else:
    with open(outName, "w", encoding="utf-8") as o:
        o.write(output)
