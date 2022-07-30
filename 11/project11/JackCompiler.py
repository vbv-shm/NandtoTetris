import sys
import Tokenizar
import os
import compilationengine as CE
import xml.etree.ElementTree as ET
import ST
import cw

def main(): 
    print(sys.argv[1])
    if os.path.isdir(sys.argv[1]):
        for all_files in os.listdir(sys.argv[1]):
            if all_files.endswith(".jack"):
                jt_object=Tokenizar.JackTokenizer(os.path.join(os.getcwd(),sys.argv[1].split("\\")[-1],all_files))
                jt_object.xml_generator()
                ce_object=CE.Ce(jt_object.tokens_list,jt_object.elements_list,all_files)
                tree=ce_object.engineStart()
                x=cw.CodeWriter(tree)
                x.generate_vm_code()
                with open (os.path.join(os.getcwd(),sys.argv[1].split("\\")[-1],all_files.split('.')[0])+".vm", "w") as file :
                    file.write(x.vm_code_main)


    else:
    
        jt_object=Tokenizar.JackTokenizer(os.path.join(os.getcwd(),sys.argv[1]))
        
        jt_object.xml_generator()
        
        ce_object=CE.Ce(jt_object.tokens_list,jt_object.elements_list,sys.argv[1].split("\\")[-1])
        
        tree=ce_object.engineStart()
        print (ET.tostring(tree, encoding='unicode'))

        x=cw.CodeWriter(tree)
        x.generate_vm_code()
        # print(x.class_table)
        with open(sys.argv[1].split(".")[0]+".vm","w") as file:
            file.write(x.vm_code_main)

        # for location,child in enumerate(tree):
        #         if child.tag=="classVarDec":
        #             print(child)

        # print(enumerate(tree))
        # element_list=list(tree.iter('subroutineDec'))
        # for child in element_list:
        #     if child[0].text=="constructor":
        #         print(child)
        # # element_list2=list(tree.iter())
        # # print(element_list2)
        # # print(element_list2[1].text)
        # for child in element_list:
            
        #         for inner_child in child:
        #             if inner_child.tag=="subroutineBody":
        #                 for iiner_child in inner_child:
        #                     if iiner_child.tag=="statements":
        #                         print(iiner_child)

            #         print(inner_child)
            #         print(inner_child)
            # elif child.text=="function":

            # elif child.text=="method":



            


# def printChild(child):
#     print(child)
    
if __name__=="__main__":
    main()