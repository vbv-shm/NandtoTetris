import os
import xml.etree.ElementTree as ET

root = ET.Element("tokens")
# root.text="TEXTtoken"

a1=ET.Element("a1")
# a1.text="TEXTa1"
a2=ET.Element("a2")
a2.text="TEXTa2"

b1=ET.Element("b1")
b1.text="TEXTb1"

root.append(a1)
root.append(a2)

a1.append(b1)

tree = ET.ElementTree(root)

root2 = ET.Element("tokens2")
root2.append(root)
tree2 = ET.ElementTree(root2)

ET.indent(tree2, space=' ', level=0)
with open("rough.xml","wb") as file:
    tree2.write(file)

root = ET.Element("tokens")
a1=ET.Element("a1")
root.append(a1)
a1=ET.Element("a2")
tree2 = ET.ElementTree(root)
ET.indent(tree2, space=' ', level=0)
with open("rough2.xml","wb") as file:
    tree2.write(file)

x="abc"
x.st

import os
os.path.abspath