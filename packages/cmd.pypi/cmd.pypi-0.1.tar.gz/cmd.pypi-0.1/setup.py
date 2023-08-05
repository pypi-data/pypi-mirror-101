
__all__=["QQ"]

class pip:

    def __new__(cls): # 不備呼叫
        print("class pip")

        if  not "this" in dir(cls):
            # print("@PIP 執行@222")
            cls.this = super().__new__(cls)
            # cls.this.cls = cls
            return cls.this.pip("twine")
        else:
            pass

    def pip(self,name="twine"):   ## 自訂參數!! @方法
        # print("@PIP 執行@666",  not "this" in dir(self.cls),id(self))


        print("self pip")
        # self.thisBL = self ### 取消-->會指令失敗-->還是限定一個 self OK
        ############################### thisBL 限定跑一次
        if  not "thisBL" in dir(self):
            self.thisBL = self
            ##################################################################
            import platform ,os
            self.linuex = (False) if (platform.system()=="Windows") else (True)
            ### linux 環境
            if  self.linuex:   
                import os
                # print(name in  [i.split(" ")[0] for i in os.popen("pip list").readlines() ])
                if  not name in [i.split(" ")[0] for i in os.popen("pip list").readlines() ]:
                    # print("尚未安裝",name,"模組套件")
                    os.system("pip install "+name+r"> /dev/nul")
                    pass
                # else:
                #     print("找到",name,"已經安裝完成")
                #     pass
            

            # ###### 上傳
            # # print("@PIP 執行@")
            # os.system(r"twine upload dist/*")
            # return self  ###########################
            # ################ 下一個建構子 必須是接收(物件) 
        return self


        


class pypirc:

      def __new__(cls): # 不備呼叫
          print(f"class pypirc {cls.path}")
          text= '''[pypi]
repository: https://upload.pypi.org/legacy/
username: moon-start
password: Moon@516'''


          if  not "this" in dir(cls):
              cls.this = super().__new__(cls).pip("twine")
              return cls.this.pypirc( text )  
          else:
              pass


      def pypirc(self,nano):
          print("self pypirc")
          ##############
          import platform 
          self.linuex = (False) if (platform.system()=="Windows") else (True)
          ### linux 環境
          if  self.linuex:   
              with open( '/root/.pypirc' , 'w+' ,encoding='utf-8') as f:
          
                  ## 寫入
                  f.seek(0,0) ## 規0
                  nano=[ i.strip()+'\n' for i in nano.split('\n') ]
                  f.writelines( nano ) ## 建檔內容

          return self  ###########################
          ################ 下一個建構子 必須是接收(物件) 
        



class MD:

      def __new__(cls): # 不備呼叫
          print(f"class MD")
          text= '''
          # /content/cmd.py/README.md'
          '''

          if  not "this" in dir(cls):
              cls.this = super().__new__(cls).pip("twine")
              return cls.this.MD( text )  
          else:
              pass

       

      def MD(self,nano):
          print("self MD")
          ##############
          import platform 
          self.linuex = (False) if (platform.system()=="Windows") else (True)
          ### linux 環境
          if  self.linuex:   
              with open( '/content/cmd.py/README.md' , 'w+' ,encoding='utf-8') as f:
          
                  ## 寫入
                  f.seek(0,0) ## 規0
                  nano=[ i.strip()+'\n' for i in nano.split('\n') ]
                  f.writelines( nano ) ## 建檔內容

          return self  ###########################
          ################ 下一個建構子 必須是接收(物件) 


#


class sdist(MD):
      def __new__(cls,BL=True): # 不備呼叫
          print(f"class sdist {cls.path} ")
          if  not "this" in dir(cls):
              cls.this = super().__new__(cls)
              ##############################
              cls.this.cls = cls
              ##############################
              return cls.this.sdist(BL)
          else:
              pass

      
      def sdist(self,BL):
          print("self sdist")
          cls = self.cls
          PA  = self.cls.path
          ##############
          import os
          if  not os.path.isdir("/content/cmd.py"):
              os.makedirs('/content/cmd.py') ## 類似 mkdir -p
          os.chdir("/content/cmd.py")


          ## 刪除 dist 和 cmd.py.egg-info ##############################
          if os.path.isdir("dist"):
             print("@刪除 ./dist")
             os.system("rm -rf ./dist")
          ##
          info = [i for i in os.listdir() if i.endswith("egg-info")]
          if  len(info)==1:
              if os.path.isdir( info[0] ):
                 print("@刪除 ./.....info")
                 os.system(f"rm -rf ./{info[0]}")
          ##############################################################

    
          if BL:
                # CMD = r"python setup.py sdist"
                CMD = f"python {PA} sdist "
                # CMD = f"python {PA} sdist {self.cls.max}"
               

                # CMD = f"python {PA} sdist >2"
          # else:
                # CMD = r"python setup.py sdist >2"   
                # CMD = f"python {PA} sdist {self.cls.max}>2"
                

          import subprocess,io
          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
          stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')
            
          str_stdout = str(stream_stdout.read())
          str_stderr = str(stream_stderr.read())

          os.system("rm -rf 2")
          ################  正確提示 
          if  str_stdout :
          
                  print(CMD,"#1 ",str_stdout)
                  # return str_stdout
                
          else:
          ################  錯誤輸出
              # if  str_stderr == "" :
              #     print("\n###",CMD,cls.CC !=CMD,"#3 cls() ")
              #     cls.BL=True             ## 新增 

              #     cls()                   ## 呼叫
              # else:
                  # print(CMD,"#1 ",str_stdout)
                  print("\n###",CMD,"#2 ",  str_stderr)
                  # return  str_stderr
          


          
          ###### 上傳 [dist/*]
          # print("@PIP 執行@")
          # os.system(r"twine upload dist/*")
          os.system("twine upload --skip-existing dist/*")
          # os.system("twine upload --skip-existing   /content/cmd.py/dist/*")
  
          return self  ###########################
          ################ 下一個建構子 必須是接收(物件) 
          # return self




# class V:

#       def __new__(cls): # 不備呼叫
#           print(f"class V")
#           # text= '''
#           # # /content/cmd.py/README.md'
#           # '''

#           text="XX"
#           if  not "this" in dir(cls):
#               cls.this = super().__new__(cls)
#               cls.this.max = cls.max
#               cls.this.FF  = cls.path
#               return cls.this.self( text )  
#           pass

#       def self(self,nano):
#           ##############
#           import platform 
#           self.linuex = (False) if (platform.system()=="Windows") else (True)
#           ### linux 環境
#           if  self.linuex:   
#               # with open( '/content/cmd.py/PPP.py' , 'r+' ,encoding='utf-8') as f:
#               with open( self.FF , 'r+' ,encoding='utf-8') as f:
              
#                   ## 讀取
#                   SS= f.readlines()
#                   N=0
#                   for  i in range(len( SS )):
                          
#                        ## N設計 is 要讀取第二次的find
#                        if SS[i].find("## version")!=-1:
#                           if  N:
#                               # print("#max : ",self.max)
#                               # print("#@",SS[i+1])  ## 列印--下一行
                              
#                               import re
#                               # print("!@### ",re.sub("\d*\.\d*", str(self.max) , SS[i+1] ) )
#                               SS[i+1] = re.sub("\d*\.\d*", str(self.max) , SS[i+1] ) 
#                               break
#                           else:
#                             N=1  
#                   ## 寫入
#                   f.seek(0,0) ## 規0
#                   # nano=[ i.strip()+'\n' for i in nano.split('\n') ]
#                   # f.writelines( nano ) ## 建檔內容
#                   f.writelines( SS ) ## 建檔內容
#                   # f.flush()
#                   # f.close()

#           return self  ###########################
#           ################ 下一個建構子 必須是接收(物件)


class mkdir:
      def __new__(cls,BL=True): # 不備呼叫
          # print(f"class mkdir {cls.path} ")
          print(f"class mkdir 1 ")
          if  not "this" in dir(cls):
              cls.this = super().__new__(cls)
              ##############################
              cls.this.cls = cls
              cls.this.FF  = cls.path
              ##############################
          
              return cls.this.self()
          pass

      def self(self):
          print(f"self mkdir 2")
 
          import platform 
          self.linuex = (False) if (platform.system()=="Windows") else (True)
          ### linux 環境
          if  self.linuex:   
              with open( self.FF , 'r' ,encoding='utf-8') as f:
            
#               # with open( '/content/cmd.py/PPP.py' , 'r+' ,encoding='utf-8') as f:
#               with open( self.FF , 'r+' ,encoding='utf-8') as f:
              
                  ## 讀取
                  SS= f.readlines()
                  for  i in range(len( SS )):
                          
                       if   SS[i].strip().startswith("packages"):
                            ## 題目
                            ##  packages=find_packages(include=['cmds','cmds.*']),
                            if   len(SS[i].strip().split(r"="))==3:
                                
                                 
                                 ## mkdir -p
                                 import os , re
                                 if   len(re.findall("[\'\"]([0-9a-zA-Z]+)\.\*[\'\"]",SS[i]))==1:
                                      DD = re.findall("[\'\"]([0-9a-zA-Z]+)\.\*[\'\"]",SS[i])[0] 
                                      path = os.path.dirname( self.FF ) + os.sep + DD                                
                                      
                                      ## 如果最後的目標 cmds 存在...則會錯誤 
                                      # os.makedirs( path, 0755 )     ## 錯誤
                                      # os.makedirs( path, mode=0o755)  ## 正確
                                      if not os.path.isdir( path ):
                                         print(f"建立 mkdir {path}")
                                         os.makedirs( path, mode=0o777)  ## 正確
                                      
                                      ## 建置 __init__.py
                                      self.init( path )    
                                      break


          return self  ###########################


      
      def   init(self,QQ):

            if  type(QQ) in [str]:
                ### 檢查 目錄是否存在 
                import os
                if  os.path.isdir(QQ) & os.path.exists(QQ) :
                    ### 只顯示 目錄路徑 ----建立__init__.py
                    for dirPath, dirNames, fileNames in os.walk(QQ):
                        
                        print( "echo > "+dirPath+f"{ os.sep }__init__.py" )
                        os.system("echo > "+dirPath+f"{ os.sep }__init__.py") 
                                    
                else:
                        ## 當目錄不存在
                        print("警告: 目錄或路徑 不存在") 
            else:
                  print("警告: 參數或型別 出現問題")  



# pipV
########## sdist 預設帶入 BL=True
########## new 順行 self().. 逆回 ....所 mkdir先
class pypi(sdist,pypirc,pip,mkdir):
      
    def __new__(cls): # 不備呼叫

        import os
        os.chdir("/content/cmd.py")
        # print(sys.argv)
        # sdist("ls -al")
        
        ############################ [傳入]
        # cls.path = "/content/cmd.py"
        import sys
        cls.path = sys.argv[0]
        ###############################
    

        super().__new__(cls)
        # pip(name)
        # return  super().__new__(cls).pip( name )

      
class siteD:
      from distutils.sysconfig import get_python_lib;
      lib= get_python_lib()

          
        # return os.popen( "python setup.py sdist > 2").read()

# en('python -c "from distutils.sysconfig import get_python_lib; print( get_python_lib())"').read()

# print(f"目前最新版本 is { pipV().max } { pipV.name }")
# ########## pypi()函數 不一定每次都跑!!
# VV="1.309"

import sys

# ,cmds
if len(sys.argv)==1:
      pypi()

else:
      class pipV:
            name = "cmd.pypi"
            # name = "pk3.py"
            def __new__(cls): # 不備呼叫
                print("class pipV")
            
                CMD = f"pip install { cls.name  }==999999"
              
                import subprocess,io,re
                proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
                proc.wait()
                stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
                stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')
                  
                # str_stdout = str(stream_stdout.read())
                str_stderr = str(stream_stderr.read())
                ################  錯誤輸出    
                SS=re.sub(".+versions:\s*","[",str_stderr)
                SS=re.sub("\)\nERROR.+\n","]",SS)


                this = super().__new__(cls) 
                AR = SS[1:-1].split(",")
                if  SS[1:-1]!="0.001":
                    this.max=str(0.001)
                else:
                    # print(len(eval(SS).split(".")))
                    # print("#@@ ", SS)
                    import  math
                    a = max(eval( SS ))

                    ################################### 小位數 3個
                    b = (math.modf(a*1000)[1]+1)/1000
                    # return b
                    # print("max 最大+1: ", b)
                    # cls.max = b

                    # import  math
                    this.max = str(b)  ## ?!?!
               


                # ## 如果都尚未建置
                # # if  not max in dir(cls):
                # #     cls.max  = "0.0.0"
                # #     this.max = f"{cls.max}"
                # #     ##############
                # # else:

                # print("[SS] : ",SS[1:-1].split(","))
                # AR = SS[1:-1].split(",")

                # # if  len(AR)==1 and SS[1:-1]!="0.0.01":
                # if  SS[1:-1]!="0.1.1.1":
                #        this.max = f"0.1.1.1"
                # else:
                #     A = [  eval( i.split(".").pop(0) ) for i in AR]
                #     B = [  eval( i.split(".").pop(1) ) for i in AR if eval(i.split(".").pop(0))==max(A) ] 
                #     C = [  eval( i.split(".").pop(2) ) for i in AR if eval(i.split(".").pop(0))==max(A)  if eval(i.split(".").pop(1))==max(B)  ] 
                #     print(max(A))
                #     print(max(B))
                #     print(max(C))

                #     AA,BB,CC=max(A),max(B),max(C)
                    
                #     ## CC=0     if sele
                #     if max(C)+1==10:
                #       ####### 進位B 一律尾數01
                #       CC="01"  
                #       BB+=1
                #       if BB==10:
                #           BB=0
                #           AA+=1
                #     else:
                #       CC+=1
                            
                #     this.max = f"{AA}.{BB}.{CC}"
                
                    

                return  this

      print("\n\n@這裡 is 第二次進入:",sys.argv)
      # print( pipV.max )
      ##############################################
      from setuptools.command.install import install
      class PostCMD(install):
            """cmdclass={'install': XXCMD,'install': EEECMD }"""
            def   run(self):
                  ## 引用專屬 boos 目錄
                  # from boos import sitePY
                  # sitePY(siteD.lib)       ## 宣告內涵

                  import os
                  ## getcwd() --> /tmp/pip-install-hbr_rpcp/cmd.py 這個位置
                  # os.system(f"echo {os.getcwd()}> /usr/local/lib/python3.7/dist-packages/cmds/CC.py")

                  ## 提示
                  # BL= os.path.isdir("/usr/local/lib/python3.7/dist-packages/cmds") ## 會錯誤!???
                  # os.system(f"echo {BL}")
                  # os.chdir("/usr/local/lib/python3.7/dist-packages/cmds") ##失敗
                  
                  os.chdir("/usr/local/lib/python3.7/dist-packages")    ## 成功
                  # if  self.Linux:
                  #     os.system("echo SSS.VMx")
                      
                  # p = subprocess.Popen(r'start cmd /k "'+P.SSQ+'"', shell=True)
                  # ping 127.0.0.1 -n 5 -w 1000 >nul && rmdir /S /Q   C:\Users\moon\AppData\Local\pip\cache\wheels
                  install.run(self)


      # VV = f'{str(sys.argv[2])}'
      ##############################################
      with open("README.md", "r") as fh:
          long_description = fh.read()
      #### setup.py ################################
      from setuptools import setup, find_packages
      setup(
            name  =  f"{pipV.name}"  ,
            ## version
            version= f"{pipV().max}",
            # version= "9.405",
            # version="1.307",
            description="My CMD 模組",
            long_description=long_description,
            long_description_content_type="text/markdown",
            author="moon-start",
            author_email="login0516mp4@gmail.com",
            url="https://gitlab.com/moon-start/cmd.py",
            license="LGPL",
            ####################### 宣告目錄 #### 使用 __init__.py
            ## 1 ################################################ 
            packages=find_packages(include=['cmds','cmds.*']),
            ## 2 ###############################################
            # packages=['git','git.cmd',"git.mingw64"],
            # packages=['cmds'],
            # packages = ['moonXP'],
            # package_data = {'': ["moon"] },
            #################################
            cmdclass={
                  'install': PostCMD
            }
            #################################      
      )


#################
# QQ("sdist")
# import sys
# print(len(sys.argv))
print(__file__)

# site.py


## setup.py ## http://lierhua.top/2018/01/15/%E5%BD%92%E6%A1%A3/Python%E5%8F%91%E5%B8%83%E5%B7%A5%E5%85%B7setuptools%E7%9A%84%E7%94%A8%E6%B3%95/