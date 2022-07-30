import sys
import Tokenizar
import os
import compilationengine as CE
import xml.etree.ElementTree as ET
import ST

class CodeWriter():

    def __init__(self,xml):
        self.xml=xml
        element_list=list(xml.iter())

        self.class_name=element_list[2].text
        self.label_counter=0
        self.current_subroutine=""
        self.current_returntype=""
        self.vm_code_main=""

        self.class_table=ST.SymbolTable(xml,"class")
        self.current_subroutine_table={"name":[],"type":[],"kind":[],"number":[]}
        self.current_subroutine_name=""


    def generate_vm_code(self):
        element_list=list(self.xml.iter("subroutineDec"))
        for child in element_list:
            
            if child[0].text=="constructor":
                # print("cons")

                self.current_subroutine_name=child[2].text
                self.current_subroutine_table=ST.SymbolTable(self.xml,"constructor",child[2].text)
                
                number_of_local=0
                if "local" in self.current_subroutine_table.symboltable["kind"]:
                    for local in self.current_subroutine_table.symboltable["kind"]:
                        if local=="local":
                            number_of_local=number_of_local+1
                else:
                        number_of_local=0

                self.current_returntype=child[1].text
                
                self.vm_code_main=self.vm_code_main+"function "+self.class_name+"."+self.current_subroutine_name+" "+str(number_of_local)+"\n"
                self.vm_constructor(child,child[1].text)
                
            elif child[0].text=="function":
                # print("cons")
                self.current_subroutine_name=child[2].text
                self.current_subroutine_table=ST.SymbolTable(self.xml,"function",child[2].text)
                # print(self.current_subroutine_table.symboltable)
                number_of_local=0
                if "local" in self.current_subroutine_table.symboltable["kind"]:
                    for local in self.current_subroutine_table.symboltable["kind"]:
                        if local=="local":
                            number_of_local=number_of_local+1
                else:
                        number_of_local=0

                self.current_returntype=child[1].text
                
                self.vm_code_main=self.vm_code_main+"function "+self.class_name+"."+self.current_subroutine_name+" "+str(number_of_local)+"\n"
                self.current_returntype=child[1].text
                self.vm_function(child,child[2].text)
                

            elif child[0].text=="method":
                
                self.current_subroutine_name=child[2].text
                self.current_subroutine_table=ST.SymbolTable(self.xml,"method",child[2].text)
                number_of_local=0
                if "local" in self.current_subroutine_table.symboltable["kind"]:
                    for local in self.current_subroutine_table.symboltable["kind"]:
                        if local=="local":
                            number_of_local=number_of_local+1
                else:
                        number_of_local=0

                self.current_returntype=child[1].text
                
                self.vm_code_main=self.vm_code_main+"function "+self.class_name+"."+self.current_subroutine_name+" "+str(number_of_local)+"\n"                
                self.current_returntype=child[1].text
                self.vm_method(child,child[2].text)

    def vm_statements(self, statements):
        i=0
        for statement in statements:
                if statement.tag=="letStatement":
                    # print("let")
                    self.vm_let(statement)
                elif statement.tag=="doStatement":
                    # print("do")
                    self.vm_do(statement)
                elif statement.tag=="whileStatement":
                    # print("while")
                    self.vm_while(statement)
                elif statement.tag=="ifStatement":
                    # print("if")
                    self.vm_if(statement)
                elif statement.tag=="returnStatement":
                    self.vm_return(statement)
                i=i+1

    def vm_constructor(self,subroutine_element,return_type):
        if "argument" in self.current_subroutine_table.symboltable["kind"]:
            arguments_number=0
            for argument in self.current_subroutine_table.symboltable["kind"]:
                if argument=="argument":
                    arguments_number=arguments_number+1
        else:
            arguments_number=0
        self.vm_code_main=self.vm_code_main+"push constant "+str(arguments_number)+"\n"+"call Memory.alloc 1\npop pointer 0\n"

        for child in subroutine_element: 
            if child.tag=="subroutineBody":
                for inner_child in child:
                    if inner_child.tag=="statements":
                        self.vm_statements(inner_child)

        # self.vm_code_main=self.vm_code_main+"push pointer 0\n"

    def vm_method(self,subroutine_element,return_type):
        if "argument" in self.current_subroutine_table.symboltable["kind"]:
            arguments_number=1
            for argument in self.current_subroutine_table.symboltable["kind"]:
                if argument=="argument":
                    arguments_number=arguments_number+1
        else:
            arguments_number=1
        self.vm_code_main=self.vm_code_main+"push argument 0\npop pointer 0\n" # setting THIS to current object. current object's address is pushed onto stack at argument 0
        for child in subroutine_element: 
            if child.tag=="subroutineBody":
                for inner_child in child:
                    if inner_child.tag=="statements":
                        self.vm_statements(inner_child)
        # if return_type=="void":
        #     self.vm_code_main=self.vm_code_main+"push pointer 0\n"

    def vm_function(self,subroutine_element,return_type):
        if "argument" in self.current_subroutine_table.symboltable["kind"]:
            arguments_number=0
            for argument in self.current_subroutine_table.symboltable["kind"]:
                if argument=="argument":
                    arguments_number=arguments_number+1
        else:
            arguments_number=0

        for child in subroutine_element: 
            if child.tag=="subroutineBody":
                for inner_child in child:
                    if inner_child.tag=="statements":
                        self.vm_statements(inner_child)

        # if return_type=="void":
        #     self.vm_code_main=self.vm_code_main+"push pointer 0\n"
    def get_number_and_kind(self,name):
        kind,number,typee=self.current_subroutine_table.get_kind_and_number(name)
        if kind is None:
            kind_class,number_class,type_class=self.class_table.get_kind_and_number(name)
            return kind_class,number_class,type_class
        return kind,number,typee

    def vm_let(self,let_element):
        element_list=list(let_element.iter())
        kind,number,typee=self.get_number_and_kind(element_list[2].text)
        
        if element_list[3].text=="[":
            print(element_list[2].text)
            self.vm_code_main=self.vm_code_main+"push "+kind+" "+str(number)+ "\n"
            self.vm_expression(element_list[4])
            self.vm_code_main=self.vm_code_main+"add\n"+"pop pointer 1\n"
            for child in let_element:
                if child.tag=="expression":
                    self.vm_expression(child)
            self.vm_code_main=self.vm_code_main+"pop that 0\n"
        else:
            for child in let_element:
                if child.tag=="expression":
                    self.vm_expression(child)
            kind,number,typee=self.get_number_and_kind(element_list[2].text) 
            # print(self.current_subroutine_table.symboltable)
            # print(element_list[2].text)  
            
                
            self.vm_code_main=self.vm_code_main+"pop "+kind+" "+str(number)+ "\n"

    def vm_return(self,return_element):
        element_list=list(return_element.iter())
        print(element_list)

        if element_list[2].text==";":
            self.vm_code_main=self.vm_code_main+"push constant 0\n"

        elif element_list[2].text=="this":
            self.vm_code_main=self.vm_code_main+"push pointer 0\n"

        else:
            for child in return_element:
                if child.tag=="expression":
                    self.vm_expression(child)

        self.vm_code_main=self.vm_code_main+"return\n"
        # if element_list[2].text==";":
        #    self.vm_code_main=self.vm_code_main+"pop temp 0\n" 



    def vm_if(self,if_element):
        element_list=list(if_element.iter())
        for child in if_element:
            if child.tag=="expression":
                self.vm_expression(child)
                break

        lc1=self.class_name+"."+self.current_subroutine_name+"."+str(self.label_counter)
        self.label_counter=self.label_counter+1
        lc2=self.class_name+"."+self.current_subroutine_name+"."+str(self.label_counter)
        self.label_counter=self.label_counter+1

        self.vm_code_main=self.vm_code_main+"not\nif-goto IF."+lc1+"\n"
        for child in if_element:
            if child.tag=="statements":
                self.vm_statements(child)
                break
        self.vm_code_main=self.vm_code_main+"goto IF."+lc2+"\n"
        self.vm_code_main=self.vm_code_main+"label IF."+lc1+"\n"
        
        if "else" in [x.text for x in element_list]:
            x=0
            for child in if_element:
                if child.tag=="statements" and x==0:
                    x=x+1
                elif child.tag=="statements" and x==1:
                    
                    self.vm_statements(child)
        self.vm_code_main=self.vm_code_main+"label IF."+lc2+"\n"

    def vm_while(self,while_element):
        lc1=self.class_name+"."+self.current_subroutine_name+"."+str(self.label_counter)
        self.label_counter=self.label_counter+1
        lc2=self.class_name+"."+self.current_subroutine_name+"."+str(self.label_counter)
        self.label_counter=self.label_counter+1


        
        self.vm_code_main=self.vm_code_main+"label WHILE."+lc1+"\n"

        for child in while_element:
            if child.tag=="expression":
                self.vm_expression(child)
                break

        self.vm_code_main=self.vm_code_main+"not\nif-goto WHILE."+lc2+"\n"
        for child in while_element:
            if child.tag=="statements":
                self.vm_statements(child)
                break
        self.vm_code_main=self.vm_code_main+"goto WHILE."+lc1+"\n"
        self.vm_code_main=self.vm_code_main+"label WHILE."+lc2+"\n"

    def vm_do(self,do_element):
        element_list=list(do_element.iter())
        # print(element_list[3].text)
        number_arguments=0
        # print("do ="+element_list[2].text)
        if element_list[3].text=="(":
            for child in do_element:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
            self.vm_code_main=self.vm_code_main+"call "+self.class_name+"."+element_list[2].text+" "+str(number_arguments+1)+"\n"
        else:
            kind,number,typee=self.get_number_and_kind(element_list[2].text)
            if kind is None:
                # print("in do none")
                for child in do_element:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
                self.vm_code_main=self.vm_code_main+"call "+element_list[2].text+"."+element_list[4].text+" "+str(number_arguments)+"\n"

            else: 
                # print("inside")
                self.vm_code_main=self.vm_code_main+"push "+kind+" "+str(number)+"\n"
                for child in do_element:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
                self.vm_code_main=self.vm_code_main+"call "+typee+"."+element_list[4].text+" "+str(number_arguments+1)+"\n"
        self.vm_code_main=self.vm_code_main+"pop temp 0\n" 


    def vm_term(self,term):

        element_list=list(term.iter())
        
        if element_list[1].tag=="integerConstant":
            self.vm_code_main=self.vm_code_main+"push constant "+element_list[1].text+ "\n"

        elif element_list[1].tag=="stringConstant":
            self.vm_code_main=self.vm_code_main+"push constant "+str(len(element_list[1].text))+ "\n"
            self.vm_code_main=self.vm_code_main+"call String.new 1"+ "\n"
            for i in range(len(element_list[1].text)):
                self.vm_code_main=self.vm_code_main+"push constant "+str(ord(element_list[1].text[i]))+ "\n"
                self.vm_code_main=self.vm_code_main+"call String.appendChar 2\n"

        elif element_list[1].text=="true" or element_list[1].text=="false" or element_list[1].text=="null":
            if element_list[1].text=="true":
                self.vm_code_main=self.vm_code_main+"push constant 1\nneg\n"
            elif element_list[1].text=="false":
                self.vm_code_main=self.vm_code_main+"push constant 0\n"
            elif element_list[1].text=="null":
                self.vm_code_main=self.vm_code_main+"push constant 0\n"

        elif element_list[1].text=="(":
            self.vm_expression(element_list[2]) #as everything inside bracket will be considered as expression

        elif element_list[1].text=="-" or element_list[1].text=="~":
            self.vm_term(element_list[2])
            if element_list[1].text=="-":
                self.vm_code_main=self.vm_code_main+"neg\n"
            elif element_list[1].text=="~":
                self.vm_code_main=self.vm_code_main+"not\n"
        
        elif len(element_list)>2 and element_list[2].text=="(":
            for child in term:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
            self.vm_code_main=self.vm_code_main+"call "+self.class_name+" "+element_list[1].text+" "+str(number_arguments+1)+"\n"

        elif len(element_list)>2 and element_list[2].text==".":
            number_arguments=0
            kind,number,typee=self.get_number_and_kind(element_list[1].text)
            if kind is None:
                for child in term:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
                self.vm_code_main=self.vm_code_main+"call "+element_list[1].text+"."+element_list[3].text+" "+str(number_arguments)+"\n"

            else: 
                self.vm_code_main=self.vm_code_main+"push "+kind+" "+str(number)+"\n"
                for child in term:
                    if child.tag=="expressionList":
                        for inner_child in child:
                            if inner_child.tag=="expression":
                                number_arguments=number_arguments+1
                                self.vm_expression(inner_child)
                self.vm_code_main=self.vm_code_main+"call "+typee+"."+element_list[3].text+" "+str(number_arguments+1)+"\n"


        elif len(element_list)>2 and element_list[2].text=="[":
            kind,number,typee=self.get_number_and_kind(element_list[1].text)
            self.vm_code_main=self.vm_code_main+"push "+kind+" "+str(number)+ "\n"
            self.vm_expression(element_list[3])

            self.vm_code_main=self.vm_code_main+"add\n"+"pop pointer 1\n"+"push that 0\n"

        else:
            kind,number,typee=self.get_number_and_kind(element_list[1].text)
            self.vm_code_main=self.vm_code_main+"push "+str(kind)+" "+str(number)+"\n"

    def vm_expression(self,expression):
        element_list=list(expression.iter())
        list_symbol=[]
        for child in expression:
            if child.tag=="term":
                # print("expression="+child.tag)
                self.vm_term(child)
            if child.tag=="symbol":
                list_symbol.append(child.text)
        list_symbol.reverse()
        # print(list_symbol)
        for symbol in list_symbol:
            if symbol=="+":
                self.vm_code_main=self.vm_code_main+"add\n"
            elif symbol=="-":
                self.vm_code_main=self.vm_code_main+"sub\n"
            elif symbol=="*":
                self.vm_code_main=self.vm_code_main+"call Math.multiply 2\n"
            elif symbol=="/":
                self.vm_code_main=self.vm_code_main+"call Math.divide 2\n"
            elif symbol=="&":
                self.vm_code_main=self.vm_code_main+"and\n"
            elif symbol==">":
                self.vm_code_main=self.vm_code_main+"gt\n"
            elif symbol=="<":
                self.vm_code_main=self.vm_code_main+"lt\n"
            elif symbol=="=":
                self.vm_code_main=self.vm_code_main+"eq\n"
            elif symbol=="|":
                self.vm_code_main=self.vm_code_main+"or\n"
