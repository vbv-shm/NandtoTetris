print("*********************")
print(0*"@SP\nA=M\nM=0\n@SP\nM=M+1\n")
print("*********************")


for i in range(4):
    for j in range(3):
        if i==2:
            continue
        print("inside j loop with i ="+str(i))
    print("outside loop ran")


import os
print(os.getcwd())
os.chdir("..")
print(os.getcwd())
    