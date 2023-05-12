import re
md2 = "cmd div a id=card href=/link"
cmd='find_all class_="mihoyo-cookie-tips mihoyo-cookie-tips--bottom mihoyo-cookie-tips--pc" id="card"'


cmd_name=cmd.split(" ")[0]
print(cmd_name)

tmp=cmd.split("\"")
tmp=tmp[:-1]
print(tmp)
args=[]
for i in tmp[0].split(" ")[1:]:
    if "=" in i:
        break
    args.append(i)
key=[]
value=[]
for i in range(len(tmp)):
    if i%2==0:
        key.append(tmp[i].split(" ")[-1].split("=")[0])
        print("a"+tmp[i].split(" ")[-1].split("=")[0])
    else:
        value.append(tmp[i])
        print("b"+tmp[i])
kwargs=dict(zip(key,value))



print(args)
print(kwargs)
