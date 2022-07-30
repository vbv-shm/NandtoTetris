import sys


def airthmaticWriter(command,jump_counter):
    assembly_code="empty\n"
    if command=="add":
        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D+M\nM=D\n@SP\nM=M+1\n"
    elif command=="neg":
        assembly_code="@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n"
    elif command=="sub":
        assembly_code="@SP\nM=M-1\nA=M\nD=-M\n@SP\nM=M-1\nA=M\nD=D+M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif command=="eq":
        True_label="eq.true."+str(jump_counter)
        continue_label="eq.continue."+str(jump_counter)
        assembly_code="@SP\nM=M-1\nA=M\nD=-M\n@SP\nM=M-1\nA=M\nD=D+M\n@"+True_label+"\nD;JEQ\n@SP\nA=M\nM=0\n@"+continue_label+"\n0;JMP\n("+True_label+")\n@SP\nA=M\nM=-1\n("+continue_label+")\n@SP\nM=M+1\n"

    elif command=="lt":
        True_label="lt.true."+str(jump_counter)
        continue_label="lt.continue."+str(jump_counter)
        assembly_code="@SP\nM=M-1\nA=M\nD=-M\n@SP\nM=M-1\nA=M\nD=D+M\n@"+True_label+"\nD;JLT\n@SP\nA=M\nM=0\n@"+continue_label+"\n0;JMP\n("+True_label+")\n@SP\nA=M\nM=-1\n("+continue_label+")\n@SP\nM=M+1\n"

    elif command=="gt":
        True_label="gt.true."+str(jump_counter)
        continue_label="gt.continue."+str(jump_counter)
        assembly_code="@SP\nM=M-1\nA=M\nD=-M\n@SP\nM=M-1\nA=M\nD=D+M\n@"+True_label+"\nD;JGT\n@SP\nA=M\nM=0\n@"+continue_label+"\n0;JMP\n("+True_label+")\n@SP\nA=M\nM=-1\n("+continue_label+")\n@SP\nM=M+1\n"

    elif command=="not":
        assembly_code="@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n"

    elif command=="and":
        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M&D\n@SP\nM=M+1\n"

    elif command=="or":

        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n"

    return "// "+command+"\n"+assembly_code


def popWriter(value,location):
    assembly_code="empty\n"
    if location=="local":
        assembly_code="@LCL\nD=M\n@"+value+"\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
    elif location=="this":
        assembly_code="@THIS\nD=M\n@"+value+"\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
    elif location=="that":
        assembly_code="@THAT\nD=M\n@"+value+"\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
    elif location=="argument":
        assembly_code="@ARG\nD=M\n@"+value+"\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
    elif location=="temp":
        assembly_code="@5\nD=A\n@"+value+"\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
    elif location=="pointer" and value=="0":
        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"
    elif location=="pointer" and value=="1":
        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
    elif location=="static":
        if "/" not in sys.argv[1].split(".")[0]:
            file_name=sys.argv[1].split(".")[0]
        else:
            file_name=sys.argv[1].split(".")[0].split("/")[-1]
        static_variable=file_name+"."+value
        assembly_code="@SP\nM=M-1\nA=M\nD=M\n@"+static_variable+"\nM=D\n"
    return "//pop "+location+" "+value+"\n"+assembly_code

    
def pushWriter(value,location):
    assembly_code="empty\n"
    if location =="constant":
        assembly_code="@"+value+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location =="local":
        assembly_code="@LCL\nD=M\n@"+value+"\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="this":
        assembly_code="@THIS\nD=M\n@"+value+"\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="that":
        assembly_code="@THAT\nD=M\n@"+value+"\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="argument":
        assembly_code="@ARG\nD=M\n@"+value+"\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location =="temp":
        assembly_code="@5\nD=A\n@"+value+"\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="pointer" and value=="0":
        assembly_code="@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="pointer" and value=="1":
        assembly_code="@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif location=="static":
        if "/" not in sys.argv[1].split(".")[0]:
            file_name=sys.argv[1].split(".")[0]
        else:
            file_name=sys.argv[1].split(".")[0].split("/")[-1]
        static_variable=file_name+"."+value
        assembly_code="@"+static_variable+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    return "//push "+location+" "+value+"\n"+assembly_code


def writer(parsed_dict,count,jump_counter):

    if count==0:
        with open(sys.argv[1].split(".")[0]+".asm","w") as file:
            file.write("")

    with open(sys.argv[1].split(".")[0]+".asm","a") as file:
        if parsed_dict["Command_type"]=="C_Airthmatic":
            file.writelines(airthmaticWriter(parsed_dict["Command_Name"],jump_counter))
        elif parsed_dict["Command_type"]=="C_Pop":
            file.writelines(popWriter(parsed_dict["pop_value"],parsed_dict["pop_location"]))
        elif parsed_dict["Command_type"]=="C_Push":
            file.writelines(pushWriter(parsed_dict["push_value"],parsed_dict["push_location"]))

