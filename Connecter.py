'''
Created on 2014-1-30

@author: bell
'''
import urllib
import urllib2

import Cipher
import Const
import time
from XMLParser import SAXParser, DOMParser
import logging

# post data to server and parse response

logger = logging.getLogger('MALogger')
saxParser = SAXParser()
domParser = DOMParser()
class poster():

    def __init__(self, location,username):
        self.__location = location
        self.__server = getattr(Const, 'SERVER_ADDRESS')[location]
        self.__header = self.__create_http_header()
        self.__cipher = Cipher.Crypter(location,username)

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
            self.__poster.updata_header('Cookie', self.__cookie)
            return True
        else:
            return False
        
    def login(self, username='', passwd=''):
        _username=self.__username or username
        _passwd = self.__passwd or passwd
        if self.__read_seesion():
            logger.info('recover')
        else:
            logger.info('login')
            _postdata = {'login_id': _username,
                     'password': _passwd
                     }
            _url='check_inspection'
            logger.debug('send check inspection')
            _content, _header = self.__poster.post(_url)
            if 'Set-Cookie' in _header:
                _tmp=_header['Set-Cookie'].split(',')
                self.__cookie = _tmp[len(_tmp)-1].split(';')[0].lstrip(' ')
            logger.debug('Cookie=%s' % (self.__cookie))
            self.__poster.updata_header('Cookie', self.__cookie)
            _url='login'
            logger.debug('send login')
            return self.__poster.post(_url
                                                   , postdata=_postdata)
    
    def post(self,destination,postdata={},parser,list,use_2nd_key=False):
        _url = self.__server + getattr(Const,'APP_ADDRESS')[destination]
        _data = None
        _use_2nd_key=False
        time.sleep(1)
        if destination in ['login','menu']:
            pass
        else:
            _use_2nd_key=True
        response=self.__do_post(_url, postdata)
        _dec=self.__decrypt(response,use_2nd_key or _use_2nd_key)
        try:
            return self.__parse(parser,_dec,list)
        except RuntimeError:
            _dec=self.__decrypt(response, not (use_2nd_key or _use_2nd_key))
            try:
                _list={'error_code':None}
                resp = self.__parse(parser,_dec,_list)['error_code']
                if '0' == resp or None == resp:
                    return self.__parse(list, _dec, list)
                else:
                    self.__relogin()
                    post(destination,)
            except:
                self.__relogin()
            
    def __relogin(self):
        logger.debug('session time out')
        os.remove(self.__session_file)
        logger.info('try to relogin')
        self.login()
        
    def __do_post(self, url, postdata={}):
        if {} != postdata:
            _data = urllib.urlencode(self.__encode_post_para(postdata,_use_2nd_key))
        request = urllib2.Request(_url, headers=self.__header, data=_data)
        response = urllib2.urlopen(request)
        return respoAnse

    def __encode_post_para(self, parameter,use_2nd_key):

        for each in parameter:
            parameter[each] = self.__cipher.encode_one_para(parameter[each],use_2nd_key)

        return parameter
    
    def updata_header(self, header, data):
        self.__header[header] = data
        
    def __parse(self,parser,content,list):
        if 'sax' == parser:
            return saxParser.start_parse(content,list)
        else:
            return domParser.start_parse(conten,list)
        
    def __decrypt(self,response,use_2nd_key):
        
        if use_2nd_key:
            return self.__cipher.decrypt_2nd((response.read()))
        else:
            return self.__cipher.decrypt((response.read()))