'''
Created on 2014-1-30

@author: bell
'''
import Connecter
import Player
import Const
import os
import logging

logger = logging.getLogger('MALogger')
class Client():

    def __init__(self, location,username):

        self.__location = location
        self.__poster = Connecter.poster(location,username)
        self.__player = Player.Player(self.__poster)
        self.__session_file=getattr(Const,'SESSION')
        self.__username=''
        self.__passwd=''
    #log in
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
                self.__cookie = _header['Set-Cookie'].split(',')[1].split(';')[0].lstrip(' ')
            logger.debug('Cookie=%s' % (self.__cookie))
            self.__poster.updata_header('Cookie', self.__cookie)
            _url='login'
            logger.debug('send login')
            _content, _header = self.__poster.post(_url
                                                   , postdata=_postdata)
            logger.info('get configure')
            self.__get_configure(_content)
            self.__save_session()

    def __get_configure(self, _content):
        list = {'party_name':[]}
        from XMLParser import SAXParser
        #_parser = XMLParser()
        #_parser.start_parse(_content,list)
        #list = _parser.get_data(list)
    def explore(self):
        
        try:
            self.__player.explore()
            #self.__player.fairy()
        except RuntimeError:
            logger.debug('session time out')
            os.remove(self.__session_file)
            logger.info('try to relogin')
            self.login()
        
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
        
def setlogger(consoleLogger=True,fileLogger=False):
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if fileLogger:
        _fileHandler=logging.FileHandler(filename=getattr(Const,'LOGFILE'))
        _fileHandler.setFormatter(_formatter)
        _fileHandler.setLevel(getattr(Const,'NOW'))
        logger.addHandler(_fileHandler)
    if consoleLogger:
        _consoleHandler=logging.StreamHandler()
        _consoleHandler.setFormatter(_formatter)
        _consoleHandler.setLevel(getattr(Const,'NOW'))
        logger.addHandler(_consoleHandler)
    
if __name__ == '__main__':

    setlogger()
    MA_client = Client('jp',username)
    MA_client.login(username, passwd)

    MA_client.explore()
