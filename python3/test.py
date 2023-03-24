#movabs rcx, 0xaf64064c860233ea
##movabs rcx, 0xaf64154c86024d67
##movabs rcx, 0xaf63fe4c86022652
##movabs rcx, 0xaf64094c86023903
##movabs rcx, 0xaf63fb4c86022139
##movabs rcx, 0xaf63af4c8601a015
##movabs rcx, 0xaf63ad4c86019caf
##movabs rcx, 0xaf63ac4c86019afc
##000000013FA34101 movabs rcx,AF63B54C8601AA47

resultList=[0xaf64064c860233ea,0xaf64154c86024d67,0xaf63fe4c86022652,0xaf64094c86023903,0xaf63fb4c86022139,
        0xaf63af4c8601a015,0xaf63ad4c86019caf,0xaf63ac4c86019afc,0xAF63B54C8601AA47]


def list_index(myList,value):
    for i,v in enumerate(myList):
        if v==value:
            return i
    return -1

def FnvHash_1(cX):
    rax=0xcbf29ce484222325
    r8=0x100000001b3
    rax=rax^ord(cX)
    rax=(rax*r8)&0xffffffffffffffff
    return rax

def FnvHash(string_xx):
    rax=0xcbf29ce484222325
    r8=0x100000001b3
    for i in string_xx:
        rax=rax^ord(i)
        rax=(rax*r8)&0xffffffffffffffff
    return rax

def Crake_1():
    xStrList=['1','1','1','1','1','1','1','1','1']
    for i in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
        nRet=FnvHash_1(i)
        nIndex=list_index(resultList,nRet)
        if nIndex!=-1:
            print "index:",nIndex,"Char:",i
            xStrList[nIndex]=i
    print xStrList
Crake_1()

print "-----------------------part 2:-------------------------"
def Crack():
    file = open("api.txt") 
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            api=line.strip()
            str_in="KXCTF20189NTDLL9"+api+"9"
            nRet=FnvHash(str_in)
            if nRet==0x4f8075587499c0ff:
                print str_in
                raw_input("find it!")
                break
    file.close()
    
Crack()

print hex(FnvHash("KXCTF20189NTDLL9DbgUiContinue9"))



    
    
