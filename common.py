import base64
import datetime,json
import urllib


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

