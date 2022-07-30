import xml.etree.ElementTree as ET
import compilationengine as CE
class JackTokenizer():
    _symbols_list=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    _keywords_list=['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
    def __init__(self,filename):
        self.elements_list=[]
        self.current_token=""
        self.tokens_list=[]
        with open(filename) as file:
            for line in file:
                line=line.strip()
                if line.startswith("//"):
                    continue
                if line.startswith("/**"):
                    continue
                if line.startswith("*"):
                    continue
                if len(line)==0:
                    continue
                line=line.split("//")
                line=line[0].strip()
                print(line)
                during_string=False

                for letter in line:
                    # if during_string is True we are appending a string.
                    if letter !="\"" and during_string:
                        self.current_token=self.current_token+letter
                        continue
                    # if we recieve " symbol and during_string is True we reach at the end of the string.
                    elif letter =="\"" and during_string:
                        self.elements_list.append("\""+self.current_token)
                        self.current_token=""
                        during_string=False
                        continue
                    # if we recieve " symbol and during_string is True we reach at the start of the string.
                    elif letter =="\"" and not during_string:
                        if len(self.current_token)!=0:
                            self.elements_list.append(self.current_token)
                            self.current_token=""
                        during_string=True
                        continue
                    # If space is seen add the token which has been appended till now.
                    if letter==" ":
                        if len(self.current_token)!=0:
                            self.elements_list.append(self.current_token)
                        self.current_token=""
                        continue
                    # if some symbol is found, add the token which has been appended till now and then add the symbol.
                    for symbol in JackTokenizer._symbols_list:
                        if symbol==letter:
                            if len(self.current_token)!=0:
                                self.elements_list.append(self.current_token)
                            self.elements_list.append(letter)
                            self.current_token=""
                            break
                    if symbol==letter:
                        continue

                    # if nothing else happens just append to string
                    self.current_token=self.current_token+letter


    def xml_generator(self):
        root = ET.Element("tokens") # make an element named named token, and make root point to it
        for token in self.elements_list:
            if token in self._symbols_list:
                e=ET.Element("symbol") # make an element named named symbol and make e point to it
                root.append(e) # attach e(pointing to XML element named symbol) to  root
                if token=="<":
                    token="&lt;"
                elif token==">":
                    token="&gt;"
                elif token=="\"":
                    token="&quot;"
                elif token=="&":
                    token="&amp;"                                                          
                e.text=token # write text of element e equal to token

                self.tokens_list.append("symbol")
                continue
            elif token in self._keywords_list:
                e=ET.Element("keyword")
                root.append(e)
                e.text=token
                self.tokens_list.append("keyword")
                continue
            elif token.startswith("\""):
                e=ET.Element("stringConstant")
                root.append(e)
                e.text=token[1:]
                self.tokens_list.append("stringConstant")
                continue
            elif token.isdigit():
                e=ET.Element("integerConstant")
                root.append(e)
                e.text=token
                self.tokens_list.append("integerConstant")
                continue
            else:
                e=ET.Element("identifier")
                root.append(e)
                e.text=token
                self.tokens_list.append("identifier")
                continue
        tree = ET.ElementTree(root)
        # ET.indent(tree, space=' ', level=0)
        with open ("new.xml", "wb") as files :
            tree.write(files)

                        

# jt_object=JackTokenizer("Main.jack")
# jt_object.xml_generator()
# print(jt_object.elements_list)
# print(jt_object.tokens_list)

# ce_object=CE.Ce(jt_object.tokens_list,jt_object.elements_list)
# ce_object.engineStart()
# for (symbol,sym_name) in zip(jt_object.tokens_list,jt_object.elements_list):
#     print(symbol+" "+sym_name)