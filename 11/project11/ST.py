class SymbolTable():

    def __init__(self,xml_data,type_table,subroutine_name=None):
        element_list=list(xml_data.iter())
        class_name=element_list[2].text

        if type_table=="class":
            self.symboltable={"name":[],"type":[],"kind":[],"number":[]}

            field_counter=0
            static_counter=0
            argument_counter=0
            local_counter=0
            parameter_counter=0

            for location,child in enumerate(element_list):
                if child.tag=="classVarDec":
                    i=0
                    while(True):
                        self.symboltable['kind'].append(element_list[location+1].text)
                        self.symboltable['type'].append(element_list[location+2].text)
                        self.symboltable['name'].append(element_list[location+3+i].text)
                        if element_list[location+1].text=='field':
                            self.symboltable['number'].append(field_counter)
                            field_counter=field_counter+1
                        elif element_list[location+1].text=='static':
                            self.symboltable['number'].append(static_counter)
                            static_counter=static_counter+1
                        if element_list[location+4+i].text==";":
                            break
                        i=i+2
                    
        elif type_table=="function":
            self.symboltable={"name":[],"type":[],"kind":[],"number":[]}
            element_list=list(xml_data.iter())

            field_counter=0
            static_counter=0
            argument_counter=0
            local_counter=0

            comma_count=0
            current_subroutine=""

            parameter_counter=0

            for location,child in enumerate(element_list):
                i=0
                
                if child.tag=="subroutineDec":
                        current_subroutine=element_list[location+3].text
                if child.tag=="varDec" and current_subroutine==subroutine_name:
                    while(True):
                        self.symboltable['kind'].append("local")
                        self.symboltable['type'].append(element_list[location+2].text)
                        self.symboltable['name'].append(element_list[location+3+i].text)
                        self.symboltable['number'].append(local_counter)
                        local_counter=local_counter+1
                        if element_list[location+4+i].text==";":
                            break
                        i=i+2

                elif child.tag=="parameterList"and current_subroutine==subroutine_name:
                    while(element_list[location+2*argument_counter+1+comma_count].text!=")"):
                        self.symboltable['kind'].append("argument")
                        self.symboltable['type'].append(element_list[location+1+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['name'].append(element_list[location+2+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['number'].append(argument_counter)
                        argument_counter=argument_counter+1
                        if argument_counter==1:
                            parameter_counter=1
                        if argument_counter>1:
                            comma_count=comma_count+1
        elif type_table=="method":
            field_counter=0
            static_counter=0
            argument_counter=0
            local_counter=0

            parameter_counter=0
            comma_count=0
            current_subroutine=""
            element_list=list(xml_data.iter())
            
            self.symboltable={"name":["this"],"type":[class_name],"kind":["argument"],"number":[0]}
            for location,child in enumerate(element_list):
                i=0
                if child.tag=="subroutineDec":
                    current_subroutine=element_list[location+3].text
                if child.tag=="varDec"and current_subroutine==subroutine_name:
                    while(True):
                        self.symboltable['kind'].append("local")
                        self.symboltable['type'].append(element_list[location+2].text)
                        self.symboltable['name'].append(element_list[location+3+i].text)
                        self.symboltable['number'].append(local_counter)
                        local_counter=local_counter+1
                        if element_list[location+4+i].text==";":
                            break
                        i=i+2
                elif child.tag=="parameterList" and current_subroutine==subroutine_name:
                    while(element_list[location+2*argument_counter+1+comma_count].text!=")"):
                        self.symboltable['kind'].append("argument")
                        self.symboltable['type'].append(element_list[location+1+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['name'].append(element_list[location+2+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['number'].append(argument_counter+1)
                        argument_counter=argument_counter+1
                        if argument_counter==1:
                            parameter_counter=1
                        if argument_counter>1:
                            comma_count=comma_count+1
        elif type_table=="constructor":
            self.symboltable={"name":[],"type":[],"kind":[],"number":[]}
            element_list=list(xml_data.iter())

            field_counter=0
            static_counter=0
            argument_counter=0
            local_counter=0

            comma_count=0
            current_subroutine=""

            parameter_counter=0

            for location,child in enumerate(element_list):
                if child.tag=="subroutineDec":
                    current_subroutine=element_list[location+3].text
                if child.tag=="varDec" and current_subroutine==subroutine_name:
                    self.symboltable['kind'].append(element_list[location+1].text)
                    self.symboltable['type'].append(element_list[location+2].text)
                    self.symboltable['name'].append(element_list[location+3].text)
                    self.symboltable['number'].append(local_counter)
                    local_counter=local_counter+1

                elif child.tag=="parameterList"and current_subroutine==subroutine_name:
                    while(element_list[location+2*argument_counter+1+comma_count].text!=")"):
                        self.symboltable['kind'].append("argument")
                        self.symboltable['type'].append(element_list[location+1+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['name'].append(element_list[location+2+2*argument_counter+parameter_counter+comma_count].text)
                        self.symboltable['number'].append(argument_counter)
                        argument_counter=argument_counter+1
                        if argument_counter==1:
                            parameter_counter=1
                        if argument_counter>1:
                            comma_count=comma_count+1
    def get_kind_and_number(self,name):
        if name in self.symboltable['name']:
            i=self.symboltable['name'].index(name)
            return self.symboltable['kind'][i],self.symboltable['number'][i],self.symboltable['type'][i]
        return None,None,None