#coding=utf-8
'''import sys,os
print __file__
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)'''
import logging
import os
ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')
import datetime,time
import xlrd

def getbrowser():
    f = open(ROOT('config/browser.txt'), 'r')
    if f:
        list=f.readlines()
        '''for line in range(0,len(list)):
            list[line]=list[line].strip()'''
        return list
    else:
        print "内容为空"
    f.close()

def openfile(filepath):
    try:
        result=[]
        f=open((filepath).decode('utf-8'),'r')
        s=f.readlines()
        for i in range(0,len(s)):
            result.append(s[i].split('\n')[0])
        logging.info("获取文件内容成功")
        return result
    except:
        logging.info("获取文件内容失败")
        raise

def get_file(path,filetype='.html',filetime=None):
    try:
        dirs=os.listdir(path)
        result=[]
        if filetime is None:
            filetime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        for i in dirs:
            #time1=(os.stat(path+'/'+i).st_ctime*1000).strftime("%Y-%m-%d")
            #获取文件修改时间的时间戳
            timestamp=int(round(os.stat(path+'/'+i).st_ctime*1000))
            #时间戳按格式转换
            time1=time.strftime(
                "%Y-%m-%d",time.localtime(timestamp/1000)
            )

            #print time1
            #print filetime
            #now=time.strftime("%Y-%m-%d",time.localtime(time.time()))
            #print now
            #if os.path.isfile(i):
            # 如果是目录 继续遍历
            if os.path.isdir(i):
                get_file(i, filetype, filetime)

            #判断文件的文件类型和小于filetime
            if os.path.splitext(i)[1]==filetype and time1==filetime:
                #存储文件的路径
                result.append(path+'/'+i)

        return result
    except:
        logging.info(u"文件为空")

#获取表格内容
def open_xls(filepath=None):
    name=[]
    rows=0
    cols=0
    try:
        ExcelFile=xlrd.open_workbook(filepath)
        #获取表格数
        sheet_names=ExcelFile.sheet_names()
        for sheet_name in sheet_names:
            sheet=ExcelFile.sheet_by_name(sheet_name)
            #print sheet.ncols,sheet.nrows
            for row in range(1,sheet.nrows):
                a = ""
                #拼接每列的值
                for col in range(0,sheet.ncols):
                    if col==0:
                        a=sheet.cell_value(row,col)
                    else:
                        a+='.'+sheet.cell_value(row,col)
                #print type(a)
                name.append(str(a))
                # case_list=str(name).replace('u\'','\'')
                # case_list.decode("unicode-escape")
        return name
    except:
        print "文件不存在"
