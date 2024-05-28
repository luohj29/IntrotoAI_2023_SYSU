#coding=utf-8
'''
0 5 15 14
7 9 6 13
1 2 12 10
8 11 4 3
'''

TXT = r"code\puzzle\ppt4.txt"
TXT_OUT = r"code\puzzle\ppt4_out.txt"
def input():
    with open(TXT, "r") as f:
        return f.read()
    
r=[]

tmp = input().split("\n")

for i in range(4):
    temp = tmp[i].split(" ")
    r+=['(at tile_%s pos_%d%d)'%(x,i+1,j+1) for j,x in enumerate(temp)]

def output():
    with open(TXT_OUT, "w") as f:
        f.write("\n".join(r))

output()