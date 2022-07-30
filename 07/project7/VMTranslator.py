import sys
from Parser_file import parser
from Code_writer import writer

def main(): 
    jump_counter=0
    print(sys.argv[1])
    with open(sys.argv[1]) as file:
        count=0
        for line in file.readlines():
            if line.startswith("//"):                   
                continue
            if line.startswith("                    "): 
                continue
            line=line.strip()
            parsed_dict=parser(line)
            print(parsed_dict)
            if len(parsed_dict.keys())!=0:
                writer(parsed_dict,count,jump_counter)
                count=count+1
                jump_counter=jump_counter+1


if __name__=="__main__":
    main()