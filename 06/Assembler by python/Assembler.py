import regex as re
import sys

final=""
SymbolsDictionary={"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24575}
Variables={}
Jump_variables={}
i=16
line_counter=0
newline=""

def preDefined(word):
    for key in SymbolsDictionary.keys():
        if key==word:
            return SymbolsDictionary[key]
    return varStore(word)

def varStore(word):
    global i
    if word in Jump_variables.keys():
        return Jump_variables[word]
    elif word in Variables.keys():
        return Variables[word]
    else:
        Variables[word]=i
        i=i+1
        return Variables[word]

def cInstruction(equation):
    s="111"
    c="nothing"
    c2="000"
    c3="000"
    if "=" in equation:
        comp=re.findall("=([!-]*[AMD0-9]+[+&|-]*[AMD0-9]*)",equation)
        if len(comp)!=0 and comp[0]=="0":
            c= "0101010"
        elif len(comp)!=0 and comp[0]=="1":
            c="0111111"
        elif len(comp)!=0 and comp[0]=="-1":
            c="0111010"
        elif len(comp)!=0 and comp[0]=="D":
            c="0001100"
        elif len(comp)!=0 and comp[0]=="A" :
            c="0110000"
        elif len(comp)!=0 and comp[0]=="!D":
            c="0001101"
        elif len(comp)!=0 and comp[0]=="!A":
            c="0110001"
        elif len(comp)!=0 and comp[0]=="-D":
            c="0001111"
        elif len(comp)!=0 and comp[0]=="-A":
            c="0110011"
        elif len(comp)!=0 and comp[0]=="A+1":
            c="0110111"
        elif len(comp)!=0 and comp[0]=="D-1":
            c="0001110"
        elif len(comp)!=0 and comp[0]=="A-1":
            c="0110010"
        elif len(comp)!=0 and comp[0]=="D+A":
            c="0000010"
        elif len(comp)!=0 and comp[0]=="D-A":
            c="0010010"
        elif len(comp)!=0 and comp[0]=="A-D":
            c="0000111"
        elif len(comp)!=0 and comp[0]=="D&A":
            c="0000000"
        elif len(comp)!=0 and comp[0]=="D|A":
            c="0010101"
        elif len(comp)!=0 and comp[0]=="D+1":
            c="0011111"
        
        elif len(comp)!=0 and comp[0]=="M":
            c="1110000"
        elif len(comp)!=0 and comp[0]=="!M":
            c="1110001"
        elif len(comp)!=0 and comp[0]=="-M":
            c="1110011"
        elif len(comp)!=0 and comp[0]=="M+1":
            c="1110111"
        elif len(comp)!=0 and comp[0]=="M-1":
            c="1110010"
        elif len(comp)!=0 and comp[0]=="D+M":
            c="1000010"
        elif len(comp)!=0 and comp[0]=="D-M":
            c="1010011"
        elif len(comp)!=0 and comp[0]=="M-D":
            c="1000111"
        elif len(comp)!=0 and comp[0]=="D&M":
            c="1000000"
        elif len(comp)!=0 and comp[0]=="D|M":
            c="1010101"
        comp2=re.findall("[;]([JLTNQEGMP]*)",equation)
        if len(comp2)!=0 and comp2[0]=="JGT":
            c2="001"
        elif len(comp2)!=0 and comp2[0]=="JEQ":
            c2="010"
        elif len(comp2)!=0 and comp2[0]=="JGE":
            c2="011"
        elif len(comp2)!=0 and comp2[0]=="JLT":
            c2="100"
        elif len(comp2)!=0 and comp2[0]=="JNE":
            c2="101"
        elif len(comp2)!=0 and comp2[0]=="JLE":
            c2="110"
        elif len(comp2)!=0 and comp2[0]=="JMP":
            c2="111"
        comp3=re.findall("([AMD]*)=",equation)
        if len(comp3)!=0 and comp3[0]=="M":
            c3="001"
        if len(comp3)!=0 and comp3[0]=="D":
            c3="010"
        if len(comp3)!=0 and comp3[0]=="MD":
            c3="011"
        if len(comp3)!=0 and comp3[0]=="A":
            c3="100"
        if len(comp3)!=0 and comp3[0]=="AM":
            c3="101"
        if len(comp3)!=0 and comp3[0]=="AD":
            c3="110"
        if len(comp3)!=0 and comp3[0]=="AMD":
            c3="111"
    else:
        comp=re.findall("([!-]*[AMD0-9]+[+&|-]*[AMD0-9]*)",equation)
        if len(comp)!=0 and comp[0]=="0":
            c= "0101010"
        elif len(comp)!=0 and comp[0]=="1":
            c="0111111"
        elif len(comp)!=0 and comp[0]=="-1":
            c="0111010"
        elif len(comp)!=0 and comp[0]=="D":
            c="0001100"
        elif len(comp)!=0 and comp[0]=="A":
            c="0110000"
        elif len(comp)!=0 and comp[0]=="!D":
            c="0001101"
        elif len(comp)!=0 and comp[0]=="!A":
            c="0110001"
        elif len(comp)!=0 and comp[0]=="-D":
            c="0001111"
        elif len(comp)!=0 and comp[0]=="-A":
            c="0110011"
        elif len(comp)!=0 and comp[0]=="A+1":
            c="0110111"
        elif len(comp)!=0 and comp[0]=="D-1":
            c="0001110"
        elif len(comp)!=0 and comp[0]=="A-1":
            c="0110010"
        elif len(comp)!=0 and comp[0]=="D+A":
            c="0000010"
        elif len(comp)!=0 and comp[0]=="D-A":
            c="0010010"
        elif len(comp)!=0 and comp[0]=="A-D":
            c="0000111"
        elif len(comp)!=0 and comp[0]=="D&A":
            c="0000000"
        elif len(comp)!=0 and comp[0]=="D|A":
            c="0010101"
        elif len(comp)!=0 and comp[0]=="D+1":
            c="0011111"
        
        elif len(comp)!=0 and comp[0]=="M":
            c="1110000"
        elif len(comp)!=0 and comp[0]=="!M":
            c="1110001"
        elif len(comp)!=0 and comp[0]=="-M":
            c="1110011"
        elif len(comp)!=0 and comp[0]=="M+1":
            c="1110111"
        elif len(comp)!=0 and comp[0]=="M-1":
            c="1110010"
        elif len(comp)!=0 and comp[0]=="D+M":
            c="1000010"
        elif len(comp)!=0 and comp[0]=="D-M":
            c="1010011"
        elif len(comp)!=0 and comp[0]=="M-D":
            c="1000111"
        elif len(comp)!=0 and comp[0]=="D&M":
            c="1000000"
        elif len(comp)!=0 and comp[0]=="D|M":
            c="1010101"
        comp2=re.findall("[;]([JLTNQEGMP]*)",equation)
        if len(comp2)!=0 and comp2[0]=="JGT":
            c2="001"
        elif len(comp2)!=0 and comp2[0]=="JEQ":
            c2="010"
        elif len(comp2)!=0 and comp2[0]=="JGE":
            c2="011"
        elif len(comp2)!=0 and comp2[0]=="JLT":
            c2="100"
        elif len(comp2)!=0 and comp2[0]=="JNE":
            c2="101"
        elif len(comp2)!=0 and comp2[0]=="JLE":
            c2="110"
        elif len(comp2)!=0 and comp2[0]=="JMP":
            c2="111"
    c=s+c+c3+c2
    return c
        
def tobin(a):
    b=bin(a).replace("0b","")
    b=str(b)
    while len(b)<15:
        b="0"+b
    return b


f=sys.argv[1]

with open(f) as file:
    for line in file.readlines():
        if line.startswith("//"):                   # removing comments
            continue
        if line.startswith("                    "): # removing empty lines
            continue
        line=line.strip()
        if not line.startswith("("):                # lines without brackets 
            if line.strip()=="":
                continue
            for word in line:
                if word==" ":
                    break
                newline=newline+word       
            newline=newline+"\n"
            line_counter=line_counter+1  
        
        if line.startswith("("):                      # lines inside ()
            temp_var=line[1:len(line)-1]      
            Jump_variables[temp_var]=line_counter     # Saving inside dictionary
            continue                                  # name and address current  
                                                      # instruction.
with open("test.hack","w") as file: 
    file.__del__
    file.write(newline)

with open("test.hack") as file:
    for line in file:
        if re.search("[@]([0-9]+)",line):
            final=final+"0"+tobin(int(re.findall("[@]([0-9]+)",line)[0]))+"\n"
        elif re.search("[@][a-zA-Z0-9.$_]+",line):
            final=final+"0"+tobin(int(preDefined(re.findall("[@]([a-zA-Z0-9$.\.\$_]+)",line)[0])))+"\n"
        else:
            final=final+str(cInstruction(line))+"\n"
f_save=".\\final\\"+f.split(".")[0]+".hack"
with open(f_save,"w") as file: 
    file.write(final.strip())

with open("test.hack","w") as file: 
    file.__del__
# print(final)
# print(Variables)
# print(newline)
print(Jump_variables)