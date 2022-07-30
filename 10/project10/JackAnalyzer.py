import sys
import Tokenizar
import os
import compilationengine as CE

print("hello")
def main(): 
    print(sys.argv[1])
    if os.path.isdir(sys.argv[1]):
        for all_files in os.listdir(sys.argv[1]):
            if all_files.endswith(".jack"):
                jt_object=Tokenizar.JackTokenizer(os.path.join(os.getcwd(),sys.argv[1].split("\\")[-1],all_files))
                jt_object.xml_generator()
                ce_object=CE.Ce(jt_object.tokens_list,jt_object.elements_list,all_files)
                ce_object.engineStart()


    else:
        print(1)
        jt_object=Tokenizar.JackTokenizer(os.path.join(os.getcwd(),all_files))
        print(1)
        jt_object.xml_generator()
        print(1)
        ce_object=CE.Ce(jt_object.tokens_list,jt_object.elements_list,sys.argv[1].split("\\")[-1])
        print(1)
        ce_object.engineStart()
        print(1)


if __name__=="__main__":
    main()