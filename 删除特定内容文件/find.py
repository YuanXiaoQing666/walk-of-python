#!/usr/bin/env python
#coding:utf8

import os
import re
from win32com.shell import shell,shellcon

#regtxt = r'.+?\.dgt'                    #扫描对象为dgt文件.
#regcontent = r'CRH380'                  #列出内容含有'CRH380'的文件
#regpath = r'C:\Users\公用\2018-799-30'  #要删除的文件夹路径
#regpath = r'C:\Users\yzq\Desktop'      #要删除的文件夹路径


print('请输入要删除的文件所在文件夹路径,'+'例如 C:\\Users\\公用\\2018-799-30')
regpath = input()  #要删除的文件夹路径

print('请输入要删除的文件中所包含的内容,'+'例如 CRH380')
regcontent = input()  #列出内容含有'CRH380'的文件

print('请输入要删除的文件格式,'+'例如 dgt')
regtxt =  '.+?\.'+input()  #扫描对象为dgt文件.


class FileException(Exception):
    pass

def deltorecyclebin(filename):
    shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))  #删除文件到回收站

def getdirlist(filepath):
    """获取目录下所有的文件."""

    txtlist = [] #文件集合.
    txtre = re.compile(regtxt)
    needfile = [] #存放结果.
    for parent, listdir, listfile in os.walk(filepath):
        for files in listfile:
            #获取所有文件.
            istxt = re.findall(txtre, files)
            filecontext = os.path.join(parent, files)
            #获取非空的文件.
            if istxt :
                txtlist.append(filecontext)
                #将所有的数据存放到needfile中.
                needfile.append(readfile(filecontext))  
    if needfile == []:
        raise FileException("no file can be find!")
    else:
        validatedata = getvalidata(needfile)
        print('\n'+'路径%s下总文件数: %s ,包含筛选内容%s的文件数: %s' %(regpath, len(txtlist),regcontent,len(validatedata)))

        print('\n'+'符合筛选条件的文件绝对路径如下:')
        print(validatedata)
        
        for i in range(len(validatedata)):
            #os.remove(validatedata[i])
            deltorecyclebin(validatedata[i])

def getvalidata(filelist=[]):
    """过滤集合中空的元素."""

    valifile = []
    for fp in filelist:
        if fp != None:
            valifile.append(fp)
    return valifile

def readfile(filepath):
    """通过正则匹配文本中内容，并返回文本."""

    flag = False
    contentre = re.compile(regcontent)
    fp = open(filepath, 'r')
    lines = fp.readlines()
    #print(lines)
    flines = len(lines)
    #print(flines)
	
    #逐行匹配数据.
    for i in range(flines): 
        iscontent = re.findall(contentre, lines[i]) 
        if iscontent:
            fp.close()
            return filepath

if __name__ == "__main__":
    getdirlist(regpath)


print('\n'+'输入任何键退出...')
input()  
