import xml.etree.ElementTree as ET
import sys
import os
class Ce():

    _symbols_list=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    _keywords_list=['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']

    def __init__(self,elements_list,tokens_list,filename):
        self.elements_list=elements_list
        self.tokens_list=tokens_list
        self.token_location=0
        self.previous_token=""
        self.filename=filename
        # for i in range(1000):
        #     self.elements_list.append("a")
        #     self.tokens_list.append("b")


    def compileClass(self):
        root = ET.Element("class")
        root.text="\n"
        
        xml=self.token_eater()
        root.append(xml)
        


        if self.elements_list[self.token_location] =="identifier":
            xml=self.token_eater()
            root.append(xml)

        else:
            print("Error at compileClass function at className")
        
        if self.tokens_list[self.token_location] =="{":
            xml=self.token_eater()
            root.append(xml)
        else:
            print("Error at compileClass, opening curly brackets required")
        
        while self.tokens_list[self.token_location] =="field" or self.tokens_list[self.token_location] =="static":
            xml_var_dec=self.compileClassVarDec()
            root.append(xml_var_dec)

        while self.tokens_list[self.token_location]=="constructor" or self.tokens_list[self.token_location]=="function"or self.tokens_list[self.token_location]=="method":
            xml_sub_def=self.compileSubroutineDec()
            root.append(xml_sub_def)

        if self.tokens_list[self.token_location] =="}":
            xml=self.token_eater()
            root.append(xml)
        else:
            print("Error at compileClass, closing curly brackets required")
        return root



    def token_eater(self):  
        # token eater is for terminal rules. And for following non-terminal rules-type, className, subRoutineName, variableName, statement or subroutinecall.
        xml_to_append=ET.Element(self.elements_list[self.token_location])
        xml_to_append.text=self.tokens_list[self.token_location]
        xml_to_append.tail="\n"
        print(self.tokens_list[self.token_location])
        self.tokenLocationMover()
        return xml_to_append

    def tokenLocationMover(self):
        self.previous_token=self.tokens_list[self.token_location]
        self.token_location=self.token_location+1
        

    def engineStart(self):
        if self.tokens_list[self.token_location]=="class":
            xml_tree=self.compileClass()
            tree = ET.ElementTree(xml_tree)
            # ET.indent(tree, space='    ', level=0)

            with open (os.path.join(os.getcwd(),sys.argv[1].split("\\")[-1],self.filename.split(".")[0])+".xml", "wb") as files :
                tree.write(files,short_empty_elements=False)

    def compileClassVarDec(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("classVarDec")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        xml=self.token_eater()
        xml_to_return.append(xml)

        # no extra xml for varName according to grammer
        xml=self.token_eater()
        xml_to_return.append(xml)

        xml=self.token_eater()
        xml_to_return.append(xml)

        while self.tokens_list[self.token_location]==",":
            xml=self.token_eater()
            xml_to_return.append(xml)
            xml=self.token_eater()
            xml_to_return.append(xml)

        # for eating ;
        xml=self.token_eater()
        xml_to_return.append(xml)
            
        return xml_to_return




    def compileSubroutineDec(self,xml_to_return=None):
        if xml_to_return== None:
                xml_to_return=ET.Element("subroutineDec")
                xml_to_return.text="\n"
                xml_to_return.tail="\n"

        if self.tokens_list[self.token_location]=="constructor" or self.tokens_list[self.token_location]=="function"or self.tokens_list[self.token_location]=="method":

            # for function type
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for function return type
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for function name
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for (
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for parameter list
            xml=self.compileParameterList()
            xml_to_return.append(xml)

            # for )
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for subRoutineBody
            xml=self.compileSubRoutineBody()
            xml_to_return.append(xml)


            return xml_to_return

    def compileParameterList(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("parameterList")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"


        if self.tokens_list[self.token_location]!=")": # checking for no parameter

            # for type
            xml=self.token_eater()
            xml_to_return.append(xml)

            # for varName
            xml=self.token_eater()
            xml_to_return.append(xml)

            while self.tokens_list[self.token_location]==",":

                # for eating ,
                xml=self.token_eater()
                xml_to_return.append(xml)

                # for type
                xml=self.token_eater()
                xml_to_return.append(xml)

                # for varName
                xml=self.token_eater()
                xml_to_return.append(xml)
            
        else:
            xml_to_return.text="\n"
            

        return xml_to_return

    def compileSubRoutineBody(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("subroutineBody")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"
        
        # for eating "{"
        xml=self.token_eater()
        xml_to_return.append(xml)

        # for varDec
        while self.tokens_list[self.token_location]=="var":
            xml=self.varDec()
            xml_to_return.append(xml)

        # for statements
        xml=self.compileStatements()
        xml_to_return.append(xml)

        # for eating }
        xml=self.token_eater()
        xml_to_return.append(xml)

        return xml_to_return
    
    def varDec(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("varDec") 
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        if self.tokens_list[self.token_location]=="var":
            # for eating var
            xml=self.token_eater()
            xml_to_return.append(xml)   

            # for eating type
            xml=self.token_eater()
            xml_to_return.append(xml)   

            # for eating varName
            xml=self.token_eater()
            xml_to_return.append(xml)  

            while self.tokens_list[self.token_location]==",":

                # for type
                xml=self.token_eater()
                xml_to_return.append(xml)

                # for varName
                xml=self.token_eater()
                xml_to_return.append(xml)       
            
        # for eating ;
            xml=self.token_eater()
            xml_to_return.append(xml)    

            return xml_to_return

    def compileStatements(self,xml_to_return= None):

        if xml_to_return== None:
            xml_to_return=ET.Element("statements")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        if self.tokens_list[self.token_location]=="let":
            xml=self.compileLet()
            xml_to_return.append(xml)
            return self.compileStatements(xml_to_return)

        elif self.tokens_list[self.token_location]=="if":
            xml=self.compileIf()
            xml_to_return.append(xml)
            return self.compileStatements(xml_to_return)

        elif self.tokens_list[self.token_location]=="while":
            xml=self.compileWhile()
            xml_to_return.append(xml)
            return self.compileStatements(xml_to_return)

        elif self.tokens_list[self.token_location]=="do":
            xml=self.compileDo()
            xml_to_return.append(xml)
            return self.compileStatements(xml_to_return)

        elif self.tokens_list[self.token_location]=="return":
            xml=self.compileReturn()
            xml_to_return.append(xml)
            return self.compileStatements(xml_to_return)
        
        return xml_to_return
    
    def compileLet(self,xml_to_return=None):
        if xml_to_return== None:
            xml_to_return=ET.Element("letStatement")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"
        
        # for eating let
        xml=self.token_eater()
        xml_to_return.append(xml)  

        # for eating varName
        xml=self.token_eater()
        xml_to_return.append(xml)  

        if self.tokens_list[self.token_location]=="[":
            # for eating [
            xml=self.token_eater()
            xml_to_return.append(xml)   

            xml=self.compileExpression()
            xml_to_return.append(xml)   

            # for eating ]
            xml=self.token_eater()
            xml_to_return.append(xml)   

        # for eating =
        xml=self.token_eater()
        xml_to_return.append(xml)   

        xml=self.compileExpression()
        xml_to_return.append(xml)

        # for eating ;
        xml=self.token_eater()
        xml_to_return.append(xml)  
        return xml_to_return

    def compileIf(self,xml_to_return=None):
        if xml_to_return== None:
            xml_to_return=ET.Element("ifStatement")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"
            

        # for eating if
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating (
        xml=self.token_eater()
        xml_to_return.append(xml) 

        xml=self.compileExpression()
        xml_to_return.append(xml)

        # for eating )
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating {
        xml=self.token_eater()
        xml_to_return.append(xml)   

        # for eating statements
        xml=self.compileStatements()
        xml_to_return.append(xml)     

        # for eating }
        xml=self.token_eater()
        xml_to_return.append(xml)      

        if self.tokens_list[self.token_location]=="else":

            # for eating else
            xml=self.token_eater()
            xml_to_return.append(xml)   

            # for eating {
            xml=self.token_eater()
            xml_to_return.append(xml)  

            # for eating statements
            xml=self.compileStatements()
            xml_to_return.append(xml) 

            # for eating }
            xml=self.token_eater()
            xml_to_return.append(xml)    

        return xml_to_return 

    def compileWhile(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("whileStatement")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        # for eating while
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating (
        xml=self.token_eater()
        xml_to_return.append(xml) 

        xml=self.compileExpression()
        xml_to_return.append(xml)

        # for eating )
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating {
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating statements
        xml=self.compileStatements()
        xml_to_return.append(xml) 

        # for eating }
        xml=self.token_eater()
        xml_to_return.append(xml) 

        return xml_to_return   

    def compileDo(self,xml_to_return=None):   

        if xml_to_return== None:
            xml_to_return=ET.Element("doStatement")  
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        # for eating do
        xml=self.token_eater()
        xml_to_return.append(xml)   

        # for eating statements
        # xml=self.compileSubRoutineCall()
        # for eating subRoutineName, className or varName
        xml=self.token_eater()
        xml_to_return.append(xml) 

        if self.tokens_list[self.token_location]==".":
            # for eating .
            xml=self.token_eater()
            xml_to_return.append(xml) 

            # for eating subRoutineName
            xml=self.token_eater()
            xml_to_return.append(xml) 

        # for eating (
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating expression list
        xml=self.compileExpressionList()
        xml_to_return.append(xml)

        # for eating )
        xml=self.token_eater()
        xml_to_return.append(xml)  

        # for eating ;
        xml=self.token_eater()
        xml_to_return.append(xml)   

        return xml_to_return        

    def compileReturn(self,xml_to_return=None):  

        if xml_to_return== None:
            xml_to_return=ET.Element("returnStatement")  
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        # for eating return
        xml=self.token_eater()
        xml_to_return.append(xml)  

        if self.tokens_list[self.token_location]!=";":
            xml=self.compileExpression()
            xml_to_return.append(xml)

        # for eating ;
        xml=self.token_eater()
        xml_to_return.append(xml)  

        return xml_to_return

    def compileExpression(self,xml_to_return=None):
        if xml_to_return== None:
            xml_to_return=ET.Element("expression")
            xml_to_return.text="\n" 
            xml_to_return.tail="\n" 

        xml=self.compileTerm()
        xml_to_return.append(xml)

        if self.tokens_list[self.token_location-1] in ["~","-"]:
            xml=self.compileTerm()
            xml_to_return.append(xml)


        else:
            while self.tokens_list[self.token_location]=="+" or self.tokens_list[self.token_location]=="-" or self.tokens_list[self.token_location]=="*" or self.tokens_list[self.token_location]=="/" or self.tokens_list[self.token_location]=="&" or self.tokens_list[self.token_location]=="|" or self.tokens_list[self.token_location]==">" or self.tokens_list[self.token_location]=="<" or self.tokens_list[self.token_location]=="=":
            
                # eating op term
                xml=self.token_eater()
                xml_to_return.append(xml)  
                
                xml=self.compileTerm()
                xml_to_return.append(xml)

        return xml_to_return

    def compileTerm(self,xml_to_return=None):
        if xml_to_return== None:
            xml_to_return=ET.Element("term") 
            xml_to_return.text="\n"
            xml_to_return.tail="\n"

        if (str(self.tokens_list[self.token_location])).isdigit():
            xml=self.token_eater()
            xml_to_return.append(xml) 
            return xml_to_return

        elif (self.tokens_list[self.token_location]).startswith("\""):
            xml=ET.Element(self.elements_list[self.token_location])
            xml.text=self.tokens_list[self.token_location][1:]
            self.tokenLocationMover()
            xml_to_return.append(xml) 
            return xml_to_return       
        elif self.tokens_list[self.token_location] in ["true","false","null","this"]:
            xml=self.token_eater()
            xml_to_return.append(xml)  
            return xml_to_return  
        elif self.tokens_list[self.token_location] in ["-","~"]:
            xml=self.token_eater()
            xml_to_return.append(xml)
            xml=self.compileTerm()
            xml_to_return.append(xml)  
            return xml_to_return 
        elif self.tokens_list[self.token_location]=="(":
            # eating ( 
            xml=self.token_eater()
            xml_to_return.append(xml)  

            xml=self.compileExpression()
            xml_to_return.append(xml)
            # eating )
            xml=self.token_eater()
            xml_to_return.append(xml)  

        else:
            if self.tokens_list[self.token_location+1]=="[":
                # eating varname
                xml=self.token_eater()
                xml_to_return.append(xml)  

                # eating [
                xml=self.token_eater()
                xml_to_return.append(xml)  

                xml=self.compileExpression()
                xml_to_return.append(xml)
                # eating ]
                xml=self.token_eater()
                xml_to_return.append(xml)  

            elif self.tokens_list[self.token_location+1]=="(" or self.tokens_list[self.token_location+1]==".":
                # for eating subRoutineName, className or varName
                xml=self.token_eater()
                xml_to_return.append(xml) 

                if self.tokens_list[self.token_location]==".":
                    # for eating .
                    xml=self.token_eater()
                    xml_to_return.append(xml) 

                    # for eating subRoutineName
                    xml=self.token_eater()
                    xml_to_return.append(xml) 

                # for eating (
                xml=self.token_eater()
                xml_to_return.append(xml) 

                # for eating expression list
                xml=self.compileExpressionList()
                xml_to_return.append(xml)

                # for eating )
                xml=self.token_eater()
                xml_to_return.append(xml) 

                return xml_to_return
            else:
                xml=self.token_eater()
                xml_to_return.append(xml) 

        return xml_to_return



    def compileSubRoutineCall(self,xml_to_return=None):

        if xml_to_return== None:
            xml_to_return=ET.Element("subRoutineCall")  
            xml_to_return.text="\n"
            xml_to_return.tail="\n"
        
        # for eating subRoutineName, className or varName
        xml=self.token_eater()
        xml_to_return.append(xml) 

        if self.tokens_list[self.token_location]==".":
            # for eating .
            xml=self.token_eater()
            xml_to_return.append(xml) 

            # for eating subRoutineName
            xml=self.token_eater()
            xml_to_return.append(xml) 

        # for eating (
        xml=self.token_eater()
        xml_to_return.append(xml) 

        # for eating expression list
        xml=self.compileExpressionList()
        xml_to_return.append(xml)

        # for eating )
        xml=self.token_eater()
        xml_to_return.append(xml) 

        return xml_to_return

    def compileExpressionList(self,xml_to_return=None):
        if xml_to_return== None:
            xml_to_return=ET.Element("expressionList")
            xml_to_return.text="\n"
            xml_to_return.tail="\n"


        if self.tokens_list[self.token_location]!=")":

            xml=self.compileExpression()
            xml_to_return.append(xml)

            while self.tokens_list[self.token_location]==",":
                
                # for eating ,
                xml=self.token_eater()
                xml_to_return.append(xml)

                xml=self.compileExpression()
                xml_to_return.append(xml)
        else:
            xml_to_return.text="\n"

        return xml_to_return








            







