
import base64
import datetime,json
import urllib
import psutil
import re
import string
import datetime
import os




#测试目录是否存在，如果不存在创建目录
def check_dir_and_create(dir_fullpath):
    if (os.path.exists(dir_fullpath)==False)||(os.path.isdir(dir_fullpath)==False):
        os.mkdir(dir_fullpath)

class DataClear:



    def text_to_datetime(self,par):
        date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}.\d{4})",par)
        try:

            date= datetime.datetime.strptime(date_all[0], "%Y-%m-%d %H:%M:%S.%f")
            return date
        except:
            return None


    def text_to_date(self,par):
        date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",par)
        try:
            date= datetime.datetime.strptime(date_all[0], "%Y-%m-%d")
            return date
        except:
            return None
    
    def text_to_int(self,par):
        try:
            rs=int(self.text_to_float(par))
            return rs
        except:
            return None

    
    def text_to_float(self,par):
        if par==None:
            return None
        num_str=re.findall(r"\d+\.?\d*",par)
        try:
            num=float(num_str[0])
            if par.find('亿')!=-1:
                num=num*100000000
            if par.find('万')!=-1:
                num=num*10000
            if par.find('%')!=-1:
                num=num*0.01
            return num
        except:
            return None
    
    



class BackSystem():
    @staticmethod
    def getpids():
        pids=psutil.pids()
        array_pids=[]
        for pidid in pids:
            pid=[]
            p = psutil.Process(pidid)
            pid.append(p.name())
            #pid.append(p.exe())
            #pid.append(p.cwd())
            pid.append(p.status())
            pid.append(p.create_time())
            #pid.append(p.uids())
            #pid.append(p.gids())
            pid.append(p.cpu_times())
            #pid.append(p.cpu_affinity())
            pid.append(p.memory_percent())
            pid.append(p.memory_info())
            pid.append(p.io_counters())
            #pid.append(p.connectios())
            pid.append(p.num_threads())
            array_pids.append(pid)
        return array_pids

    @staticmethod
    def getpids_by_name(par):
        pids=BackSystem.getpids()
        r_pids=[]
        for pid in pids:
            print(pid[0])
            if pid[0].find(par)>0:
                r_pids.append(pid)
        return r_pids


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%f')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

#编码的时候，先uri后base64，解码先base64，后uri
class Base64Uri():
    @staticmethod
    def decode(par):
        decodebase64=base64.b64decode(par.encode("utf-8")).decode("utf-8")
        decodeuri=urllib.parse.unquote(decodebase64)
        return decodeuri
    @staticmethod
    def encode(par):

        endcodebase64 =base64.b64encode(par.encode('utf-8')).decode("utf-8")
        encodeuri=urllib.parse.quote(endcodebase64)
        #encodestr = base64.b64encode(par.encode('utf-8'))
        return encodeuri


class Base64():
    @staticmethod
    def decode(par):
        return base64.b64decode(par.encode("utf-8")).decode("utf-8")
    @staticmethod
    def encode(par):
        encodestr =base64.b64encode(par.encode('utf-8')).decode("utf-8")
        #encodestr = base64.b64encode(par.encode('utf-8'))
        return encodestr

