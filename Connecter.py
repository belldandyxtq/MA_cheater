'''
Created on 2014-1-30

@author: bell
'''
import urllib
import urllib2

import Cipher
import Const
import time

# post data to server and parse response


class poster():

    def __init__(self, location,username):
        self.__location = location
        self.__server = getattr(Const, 'SERVER_ADDRESS')[location]
        self.__header = self.__create_http_header()
        self.__cipher = Cipher.Crypter(location,username)

    def __create_http_header(self):
        _header = getattr(Const, 'HEADER')
        return _header

    def post(self, destination, postdata={}):
        _url = self.__server + getattr(Const,'APP_ADDRESS')[destination]
        _data = None
        _use_2nd_key=False
        time.sleep(1)
        if destination in ['login']:
            pass
        else:
            _use_2nd_key=True
        if {} != postdata:
            _data = urllib.urlencode(self.encode_post_para(postdata,_use_2nd_key))
        request = urllib2.Request(_url, headers=self.__header, data=_data)
        response = urllib2.urlopen(request)
        
        if _use_2nd_key:
            return self.__cipher.decrypt_2nd((response.read())), response.info()
        else:
            return self.__cipher.decrypt((response.read())), response.info()

    def encode_post_para(self, parameter,use_2nd_key):

        for each in parameter:
            parameter[each] = self.__cipher.encode_one_para(parameter[each],use_2nd_key)

        return parameter

    def updata_header(self, header, data):
        self.__header[header] = data
