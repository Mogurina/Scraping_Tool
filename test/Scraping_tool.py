import urllib.robotparser
import requests as re
from bs4 import BeautifulSoup as bs
import re as r
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def flatten_list(l):
    for el in l:
        if isinstance(el, list):
            yield from flatten_list(el)
        else:
            yield el



#次回やること　デバック用のデコレータを作成し、メソッド内の全ての変数の中身を確認できる様にすること


class Scraping_Tool():#全体的に機能が違うのに名前が似通っているメソッドがある為改善すべし
    def __init__(self):
        self.Main_URL=""
        self.ROBOTS=""
        self.ROBOTS_F=False
        self.USER_AGENT="*"
        self.DIR=""
        self.response=None
        self.soup=None
        self.DATA_TMP=None
        self.DATA=None
        self.GET_DATA_TMP=None
        self.IMG_URL=None
        self.IMG_NAME=None

    def show_cmd(self):
        """使用可能なコマンド一覧を表示する"""
        cmd=[method for method in dir(Scraping_Tool) if method.startswith('_') is False]
        for i in cmd:
            print(i)
    
    def exit(self):#プログラム終了
        """プログラムを終了する。"""
        return -1

    def test(self):#コマンド実行ようテストメソッド
        """this is test method"""
        print("hello world!!")
        return 0

    def __robots_check(func):
        def wrapper(self,*args,**kwargs):
            if self.ROBOTS_F == True:
                func(self,*args,**kwargs)
            else:
                print("このサイトは許可されていません。")
        return wrapper

    def set_url(self,*args,**kwargs):
        if "url" in kwargs:
            self.Main_URL=kwargs["url"]
        else:
            try:
                self.Main_URL=args[0]
            except:
                print("url引数を指定してやり直してください")
        if self.Main_URL[-1]!="/":
            self.Main_URL+="/"
        self.robots()
        self.__get()
        #print("set_url::"+kwargs["url"])

    def get_url(self):
        return self.Main_URL

    def show_url(self):
            print(self.Main_URL)

    def root(self):
        self.__get()

    def get_root_url(self,url):
        pattern = r"(?P<root>https?://.*?)\/.*"
        result = r.match(pattern, url)
        if result is not None:
            return result.group('root')

    def get_robots_txt_path(self):
        root_url=self.get_root_url(self.Main_URL)
        return root_url + '/robots.txt'
    
    def robots_data(self):
        response=re.get(self.get_robots_txt_path())
        self.ROBOTS=response.text
        print(self.ROBOTS)

    def robots(self):
        robots_url=self.get_robots_txt_path()
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        result=rp.can_fetch(self.USER_AGENT,self.Main_URL)
        if result==True:
            print("d( *＾ω＾*)pﾔｯﾀｰ!")
        else:
            print("。*゜(PД｀ﾟ)ﾟ｡わーん")
        self.ROBOTS_F=result

    def show_all(self):
        k=self.__dict__.keys()
        for i in k: 
            print("{}: {:.50}".format(i,str(self.__dict__[i]).split("\n")[0]))
    
    @__robots_check
    def get(self,*args):
        data=[]
        for i in self.DATA_TMP:
            #print(i)
            g=i.get(args[0])
            if g != None:
                data.append(g)
        print(data)
        self.GET_DATA_TMP=data

    @__robots_check
    def save_url(self):
        self.IMG_URL=self.GET_DATA_TMP

    @__robots_check
    def save_name(self):
        self.IMG_NAME=self.GET_DATA_TMP  

    @__robots_check
    def save_img(self,**kwargs):#複雑になりすぎてるからなおすように！！！
        #print(kwargs)
        path=kwargs["path"]
        #print("path::"+path)
        if len(self.IMG_NAME)==len(self.IMG_URL):
            for i in range(len(self.IMG_URL)):
                response = re.get(self.IMG_URL[i])
                image=response.content
                #print(response)
                file_name = r.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', self.IMG_NAME[i])
                full_path=f"{path}\{file_name}.{self.IMG_URL[i].split('.')[-1]}"
                print(full_path)
                with open(full_path,"wb") as f:
                    f.write(image)
        else:
            for i in range(len(self.IMG_URL)):
                response = re.get(self.IMG_URL[i])
                image=response.content
                full_path=f"{path}\{i}.{self.IMG_URL[i].split('.')[-1]}"
                print(full_path)
                with open(full_path,"wb") as f:
                    f.write(image)

    @__robots_check
    def save_url_data(self,**kwargs):#改善の余地あり
        response = re.get(kwargs["url"])
        images=response.content
        full_path=f"{kwargs['path']}\{kwargs['name']}.{kwargs['url'].split('.')[-1]}"
        print(full_path)
        with open(full_path,"wb") as f:
            f.write(images)


    @__robots_check
    def __get(self):
        self.response=re.get(self.Main_URL)
        self.response.encoding = self.response.apparent_encoding 
        self.soup=bs(self.response.text,"html.parser")
        print(self.response)
        self.DATA_TMP=self.soup

    @__robots_check
    def find_all(self,*args,**kwargs):
        if type(self.soup) is bs:
            temp=self.soup.find_all(args,kwargs)
        else:
            temp=[]
            self.soup=flatten_list(self.soup)
            for i in self.soup:
                temp.append(i.find_all(args,kwargs))
        self.DATA_TMP=temp
        #print(type(self.soup))
        #print(type(temp))
        return temp

    @__robots_check
    def save(self):
        self.soup=self.DATA_TMP
    
    @__robots_check
    def show(self):
        print(self.DATA_TMP)
    