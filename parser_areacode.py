f=open("code.txt","r",encoding='UTF8')

a=f.readlines()
f.close()

for string in a:
    t=string[string.index(":")+2:]
    t=t.replace('code:','"code":')
    t=t.replace('codeNm:','"codeNm":')
    t=t.replace('upperCode:','"upperCode":')
    t=t.replace('engnSe:','"engnSe":')

    exec("d="+t)

    print(d["code"])
