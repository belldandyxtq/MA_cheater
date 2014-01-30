'''
Created on 2014-1-30

@author: bell
'''
import urllib
import urllib2

import Cipher
import Const

#post data to server and parse response
class poster():
    
    def __init__(self,location):
        self.__location=location
        self.__server=getattr(Const,'SERVER_ADDRESS')[location]
        self.__header=self.__create_http_header()
        self.__cipher=Cipher.Crypter(location)
        
    def __create_http_header(self):
        _header=getattr(Const,'HEADER')
        return _header
    def post(self,destination,postdata={}):
        _url=self.__server+destination
        _data=None
        if {} != postdata :
            _data=urllib.urlencode(self.encode_post_para(postdata))
        request=urllib2.Request(_url,headers=self.__header,data=_data)
        response=urllib2.urlopen(request)
        
        return self.__cipher.decrypt((response.read())),response.info()
    
    def encode_post_para(self,parameter):
        
        for each in parameter :
            parameter[each]=self.__cipher.encode_one_para(parameter[each])
            
        return parameter
    
    def updata_header(self,header,data):
        self.__header[header]=data