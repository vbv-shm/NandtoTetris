import sys
from Parser_file import parser
from Code_writer import writer
from Code_writer import dirWriter
import os

def main(): 
    print(sys.argv[1])
    if os.path.isdir(sys.argv[1]):
        print("DIR")
        vmMultipleFileOpener(sys.argv[1])
    else:
        vmSingleFileOpener(sys.argv[1])

def vmMultipleFileOpener(dir_name):
    jump_counter=0
    count=0
    files_counter=0
    for all_files in os.listdir(dir_name):
        if all_files.endswith(".vm"):
            print(os.path.join(dir_name,all_files))
            with open(os.path.join(dir_name,all_files)) as file:
                for line in file.readlines():
                    if line.startswith("//"):                   
                        continue
                    if line.startswith("                    "): 
                        continue
                    if "  " in line:
                        line=line.split("  ")[0]
                    line=line.strip()
                    parsed_dict=parser(line)
                    if parsed_dict is not None:
                        print(parsed_dict)
                        dirWriter(parsed_dict,count,jump_counter)
                        count=count+1
                        jump_counter=jump_counter+1
            # os.chdir("..")


def vmSingleFileOpener(file_name):
    jump_counter=0
    with open(sys.argv[1]) as file:
        count=0
        for line in file.readlines():
            if line.startswith("//"):                   
                continue
            if line.startswith("                    "): 
                continue
            line=line.strip()
            parsed_dict=parser(line)
            if parsed_dict is not None:
                print(parsed_dict)
                writer(parsed_dict,count,jump_counter)
                count=count+1
                jump_counter=jump_counter+1


if __name__=="__main__":
    main()