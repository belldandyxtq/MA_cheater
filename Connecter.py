'''
Created on 2014-1-30

@author: bell
'''
import urllib
import urllib2

import Cipher
import Const
import time
import os
from XMLParser import SAXParser, DOMParser
import logging

# post data to server and parse response

logger = logging.getLogger('MALogger')
saxParser = SAXParser()
domParser = DOMParser()

class Poster():

    def __init__(self, location,username,password):
        self.__location = location
        self.__username = username
        self.__passwd = password
        self.__server = getattr(Const, 'SERVER_ADDRESS')[location]
        self.__header = self.__create_http_header()
        self.__cipher = Cipher.Crypter(location,username)
        self.__session_file=getattr(Const,'SESSION')

    def __create_http_header(self):
        _header = getattr(Const, 'HEADER')
        return _header
    
    def __save_session(self):
        f=open(self.__session_file,'w')
        f.write("%s:%s" %('cookie',self.__cookie))
        f.close()
        
    def __read_seesion(self):
        if os.path.exists(self.__session_file):
            f=open(self.__session_file,'r')
            self.__cookie=f.read().split(':')[1]
            f.close()
            self.__updata_header('Cookie', self.__cookie)
            return True
        else:
            return False
        
    def login(self):
        if self.__read_seesion():
            logger.info('recover')
        else:
            logger.info('login')
            _postdata = {'login_id': self.__username,
                     'password': self.__passwd
                     }
            _url='check_inspection'
            logger.debug('send check inspection')
            try:
                _content, _header = self.post(_url)
            except:
                pass
            
            if 'Set-Cookie' in _header:
                _tmp=_header['Set-Cookie'].split(',')
                self.__cookie = _tmp[len(_tmp)-1].split(';')[0].lstrip(' ')
            logger.debug('Cookie=%s' % (self.__cookie))
            self.__updata_header('Cookie', self.__cookie)
            self.__save_session()
            _url='login'
            logger.debug('send login')
            _list={}
            return self.post(_url, parser='sax',list=_list,postdata=_postdata)
    
    def post(self,destination,parser='dom',list={},postdata={},use_2nd_key=False):
        _url = self.__server + getattr(Const,'APP_ADDRESS')[destination]
        _data = None
        time.sleep(1)
        if destination in ['login','register']:
            _use_2nd_key=False
        else:
            _use_2nd_key=True
        _response=self.__do_post(_url, postdata,use_2nd_key or _use_2nd_key)
        if destination in ['check_inspection']:
            return _response.read(),_response.info()
        _dec=self.__decrypt(_response.read(),use_2nd_key or _use_2nd_key)
        try:
            return self.__parse(parser,_dec,list),_response.info()
        except RuntimeError:
            _dec=self.__decrypt(_response.read(), not (use_2nd_key or _use_2nd_key))
            try:
                _list={'error_code':None}
                resp = self.__parse(parser,_dec,_list)['error_code']
                if '0' == resp or None == resp:
                    return self.__parse(list, _dec, list),_response.info()
                else:
                    self.__relogin()
                    self.post(destination,postdata,parser,list,use_2nd_key)
            except:
                self.__relogin()
                return self.post(destination,postdata,parser,list,use_2nd_key)
            
    def __relogin(self):
        logger.debug('session time out')
        if os.path.exists(self.__session_file):
            os.remove(self.__session_file)
        logger.info('try to relogin')
        self.login()
        
    def __do_post(self, url, postdata={},_use_2nd_key=False):
        _data=''
        if {} != postdata:
            _data = urllib.urlencode(self.__encode_post_para(postdata,_use_2nd_key))
        request = urllib2.Request(url, headers=self.__header, data=_data)
        response = urllib2.urlopen(request)
        return response

    def __encode_post_para(self, parameter,use_2nd_key):

        for each in parameter:
            parameter[each] = self.__cipher.encode_one_para(parameter[each],use_2nd_key)

        return parameter
    
    def __updata_header(self, header, data):
        self.__header[header] = data
        
    def __parse(self,parser,content,list):
        if 'sax' == parser:
            return saxParser.start_parse(content,list)
        else:
            return domParser.start_parse(content,list)
        
    def __decrypt(self,response,use_2nd_key):
        
        if use_2nd_key:
            return self.__cipher.decrypt_2nd(response)
        else:
            return self.__cipher.decrypt(response)