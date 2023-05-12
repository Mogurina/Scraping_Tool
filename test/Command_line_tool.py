import inspect
import Scraping_tool as st
import traceback

class Command_line_tool():#コマンドの実行メソッドがスパゲッティすぎるｗ
    def __init__(self,class_obj) -> None:
        self.wrap_class=class_obj
        self.CMD={}
        self.set_command(self.wrap_class)
        self.CMD_LOG=[]
        self.CMD_LOG_TMP=[]
        
    def set_command(self,class_obj):#クラス内で作成されたメソッドを自動的に辞書型に割り当てる
        obj=inspect.getmembers(class_obj, predicate=inspect.ismethod)
        #print(obj)
        cmd_n=[i[0] for i in obj]
        #print(cmd_n)
        cmd_e=[i[1] for i in obj]
        self.CMD=dict(zip(cmd_n,cmd_e))


    def show_cmd(self):
        print(self.CMD)
    
    def exe_command(self,command):#コマンド実行　引数の処理　スパゲッティすぎるがもう手が付けられない　てか付けたくない　あああああああああ
        self.CMD_LOG.append(command)
        cmd_name=command.split(" ")[0]
        tmp=command.split("\"")
        #print(tmp)
        tmp2=tmp[:-1]
        args=[]
        for i in tmp[0].split(" ")[1:]:
            if "=" in i:
                break
            args.append(i)
        key=[]
        value=[]
        for i in range(len(tmp2)):
            if i%2==0:
                key.append(tmp2[i].split(" ")[-1].split("=")[0])
                #print("a"+tmp2[i].split(" ")[-1].split("=")[0])
            else:
                value.append(tmp2[i])
                #print("b"+tmp2[i])
        kwargs=dict(zip(key,value))
        #print("command:",cmd_name)
        #print("args:",args)
        #print("kwargs:",kwargs)
        return self.EXE(cmd_name,*args,**kwargs)

    def EXE(self,cmd,*args,**kwargs):#引数によって実行する
        try:
            if len(args)>0 and len(kwargs)>0:
                #print("a&k")
                resolt=self.CMD[cmd](*args,**kwargs)
                return resolt
            elif len(args)>0:
                #print("a")
                if args[0]=="help":
                    print(self.CMD[cmd].__doc__)
                    resolt=0
                else:
                    resolt=self.CMD[cmd](*args)
                return resolt
            elif len(kwargs)>0:
                #print("k")
                resolt=self.CMD[cmd](**kwargs)
                return resolt
            else:
                #print("none")
                resolt=self.CMD[cmd]()
                return resolt
        except:
            print(f"{cmd}は存在しない、もしくは引数の指定が正しくありません。")
            traceback.print_exc()
            return 0
    
    def get_data(self,name):
        return self.wrap_class
    def reset(self):
        self.CMD_LOG=[]

    def restart(self):
        self.CMD_LOG_TMP=self.CMD_LOG
        for i in self.CMD_LOG_TMP:
            self.exe_command(i)
        self.CMD_LOG=[]
    def show_log(self):
        for i in self.CMD_LOG:
            if i != "get_url":
                print(i)

def main():
    resolt=None
    cmd=Command_line_tool(st.Scraping_Tool())
    while True:
        command=input(f"{cmd.exe_command('get_url')}>")
        if command == "log":
            cmd.show_log()
        elif command == "log_reset":
            cmd.reset()
        elif command != "":
            resolt = cmd.exe_command(command)
        if resolt==-1:
            break

if __name__=="__main__":
    main()