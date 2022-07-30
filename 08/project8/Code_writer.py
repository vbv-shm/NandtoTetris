import sys
import os


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


def labelWriter(label_name):
    assembly_code="("+label_name+")\n"
    return "// label \n"+assembly_code

def goTo(label_name):
    assembly_code="@"+label_name+"\n0;JMP\n"
    return "// goto\n"+assembly_code

def ifgoTo(label_name):
    assembly_code="@SP\nM=M-1\nA=M\nD=M\n@"+label_name+"\nD;JNE\n"
    return "// ifgoto\n"+assembly_code

def call(function_name,number_of_args,jump_counter):
    returnAdd="returnAddress."+str(jump_counter)
    # pushing return address, LCL, ARG, THIS, THAT into stack.
    assembly_code="@"+returnAdd+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    # Repositioning ARG
    assembly_code=assembly_code+"@SP\nD=M\n@5\nD=D-A\n@"+number_of_args+"\nD=D-A\n@ARG\nM=D\n"
    # Repositioning LCL
    assembly_code=assembly_code+"@SP\nD=M\n@LCL\nM=D\n"
    # Adding goto function name
    assembly_code=assembly_code+"@"+function_name+"\n0;JMP\n"
    # generating the label where we have to return.
    assembly_code=assembly_code+"("+returnAdd+")\n"
    return "// call\n"+assembly_code

def func(function_name,number_of_local,jump_counter):
    # this method(talking about python method used here to write function of our HACK language) writes function code in assembly. It is called inside of call function command by using goto command. Our ROM architecture is such that, no function ever runs without being called

    # Adding function name as label
    assembly_code="("+function_name+")\n"
    # push 0, equal to number of local variable
    # assembly_code=assembly_code+number_of_local*("@SP\nA=M\nM=0\n@SP\nM=M+1\n")
    for i in range(int(number_of_local)):
        assembly_code=assembly_code+"@SP\nA=M\nM=0\n@SP\nM=M+1\n"
    return "// function\n"+assembly_code

def returnLabel(jump_counter):

    # creating a variable endframe at register R13. R13 will point where LCL of current fucntion is pointing.
    assembly_code="@LCL\nD=M\n@R13\nM=D\n"

    # creating another variable retAddr at register R14 such that 
    # retAddr=(endFrame-5)*
    # R14 holds address of label from where the function is called or where we have to return in ROM. This label was pushed into stack during call command.
    assembly_code=assembly_code+"@R13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n"

    # On top of our stack we have value which we have to return. We will pop this value from the stack and push it where ARG is pointing. As ARG points to the first argument variable of our current function. First argument variable is the first thing we pushed onto the stack of our function call.
    assembly_code=assembly_code+"@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n"

    # Now we will move our stack pointer to ARG+1 as ARG now holds the value which was returned.
    assembly_code=assembly_code+"@ARG\nD=M+1\n@SP\nM=D\n"

    # Now we will recover our LCL, ARG, THAT and THIS of previous function(from where our current function is called)
    assembly_code=assembly_code+"@R13\nA=M-1\nD=M\n@THAT\nM=D\n@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n" 

    # Now we will go to the address stored in variable retAddr which is register R14
    assembly_code=assembly_code+"@R14\nA=M\n0;JMP\n"
    return "// return\n"+assembly_code


def writer(parsed_dict,count,jump_counter):
    if count==0:
        returnAdd="returnAddress.Sys.int"
        # pushing return address, LCL, ARG, THIS, THAT into stack.
        assembly_code="@"+returnAdd+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # Repositioning ARG
        assembly_code=assembly_code+"@SP\nD=M\n@5\nD=D-A\n@0\nD=D-A\n@ARG\nM=D\n"
        # Repositioning LCL
        assembly_code=assembly_code+"@SP\nD=M\n@LCL\nM=D\n"
        # Adding goto function name
        assembly_code=assembly_code+"@Sys.init\n0;JMP\n"
        # generating the label where we have to return.
        assembly_code=assembly_code+"("+returnAdd+")\n"
        with open(sys.argv[1].split(".")[0]+".asm","w") as file:
            # file.write("@256\nD=A\n@0\nM=D\n"+assembly_code)
            file.write("")

    with open(sys.argv[1].split(".")[0]+".asm","a") as file:
        if parsed_dict["Command_type"]=="C_Airthmatic":
            file.writelines(airthmaticWriter(parsed_dict["Command_Name"],jump_counter))

        elif parsed_dict["Command_type"]=="C_Pop":
            file.writelines(popWriter(parsed_dict["pop_value"],parsed_dict["pop_location"]))

        elif parsed_dict["Command_type"]=="C_Push":
            file.writelines(pushWriter(parsed_dict["push_value"],parsed_dict["push_location"]))

        elif parsed_dict["Command_type"]=="C_label":
            file.writelines(labelWriter(parsed_dict["label_name"]))

        elif parsed_dict["Command_type"]=="C_goto":
            file.writelines(goTo(parsed_dict["label_name"]))

        elif parsed_dict["Command_type"]=="C_ifgoto":
            file.writelines(ifgoTo(parsed_dict["label_name"]))
        elif parsed_dict["Command_type"]=="C_call":
            file.writelines(call(parsed_dict["label_name"],parsed_dict["arguments"]),jump_counter)
        elif parsed_dict["Command_type"]=="C_function":
            file.writelines(func(parsed_dict["label_name"],parsed_dict["local_variables"],jump_counter))
        elif parsed_dict["Command_type"]=="C_return":
            file.writelines(returnLabel(jump_counter))

def dirWriter(parsed_dict,count,jump_counter):
    
    if count==0:
        # os.chdir(os.path.join(os.getcwd(),sys.argv[1]))
        returnAdd="returnAddress.Sys.int"
        # pushing return address, LCL, ARG, THIS, THAT into stack.
        assembly_code="@"+returnAdd+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # Repositioning ARG
        assembly_code=assembly_code+"@SP\nD=M\n@5\nD=D-A\n@0\nD=D-A\n@ARG\nM=D\n"
        # Repositioning LCL
        assembly_code=assembly_code+"@SP\nD=M\n@LCL\nM=D\n"
        # Adding goto function name
        assembly_code=assembly_code+"@Sys.init\n0;JMP\n"
        # generating the label where we have to return.
        assembly_code=assembly_code+"("+returnAdd+")\n"
        with open(os.path.join(sys.argv[1],sys.argv[1])+".asm","w") as file:
            file.write("@256\nD=A\n@0\nM=D\n"+assembly_code)
        # os.chdir("..")

    with open(os.path.join(sys.argv[1],sys.argv[1])+".asm","a") as file:
        if parsed_dict["Command_type"]=="C_Airthmatic":
            file.writelines(airthmaticWriter(parsed_dict["Command_Name"],jump_counter))

        elif parsed_dict["Command_type"]=="C_Pop":
            file.writelines(popWriter(parsed_dict["pop_value"],parsed_dict["pop_location"]))

        elif parsed_dict["Command_type"]=="C_Push":
            file.writelines(pushWriter(parsed_dict["push_value"],parsed_dict["push_location"]))

        elif parsed_dict["Command_type"]=="C_label":
            file.writelines(labelWriter(parsed_dict["label_name"]))

        elif parsed_dict["Command_type"]=="C_goto":
            file.writelines(goTo(parsed_dict["label_name"]))

        elif parsed_dict["Command_type"]=="C_ifgoto":
            file.writelines(ifgoTo(parsed_dict["label_name"]))

        elif parsed_dict["Command_type"]=="C_call":
            file.writelines(call(parsed_dict["label_name"],parsed_dict["arguments"],jump_counter))
        elif parsed_dict["Command_type"]=="C_function":
            file.writelines(func(parsed_dict["label_name"],parsed_dict["local_variables"],jump_counter))
        elif parsed_dict["Command_type"]=="C_return":
            file.writelines(returnLabel(jump_counter))