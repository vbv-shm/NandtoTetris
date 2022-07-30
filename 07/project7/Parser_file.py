def parser(line):
    command_dict={}
    line=line.strip()
    words=line.split()
    if len(words)==0:
        return command_dict
    if len(words)==1:
        command_dict["Command_Name"]=line
        if line == "sub" or line=="add" or line=="neg" or line== "eq" or line=="gt" or line=="lt" or line=="and" or line=="or" or line=="not":
            command_dict["Command_type"]="C_Airthmatic"
            return command_dict
    else:
        command_dict["Command_Name"]=words[0]
        if words[0]=="push":
            command_dict["Command_type"]="C_Push"
            command_dict["push_location"]=words[1]
            command_dict["push_value"]=words[2]
            return command_dict
        if words[0]=="pop":
            command_dict["Command_type"]="C_Pop"
            command_dict["pop_location"]=words[1]
            command_dict["pop_value"]=words[2]
            return command_dict


            
