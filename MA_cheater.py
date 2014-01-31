'''
Created on 2014-1-30

@author: bell
'''
import Connecter
import Player
import Const
import logger
import os

class Client():

    def __init__(self, location,username):

        self.__location = location
        self.__poster = Connecter.poster(location,username)
        self.__player = Player.Player(self.__poster)
    #log in
    def login(self, username, passwd):
        if self.__read_seesion():
            return 
        else:
            _postdata = {'login_id': username,
                     'password': passwd
                     }
            _url='check_inspection'
            _content, _header = self.__poster.post(_url)
            if 'Set-Cookie' in _header:
                self.__cookie = _header['Set-Cookie'].split(',')[1].split(';')[0].lstrip(' ')
            self.__poster.updata_header('Cookie', self.__cookie)
            _url='login'
            _content, _header = self.__poster.post(_url
                                                   , postdata=_postdata)
            self.__get_configure(_content)
            self.__save_session()

    def __get_configure(self, _content):
        list = {'party_name':[]}
        from XMLParser import XMLParser
        #_parser = XMLParser()
        #_parser.start_parse(_content,list)
        #list = _parser.get_data(list)
    def explore(self):
        #self.__player.explore()
        self.__player.fairy()
        
    def __save_session(self):
        f=open('D:/million/session','w')
        f.write("%s:%s" %('cookie',self.__cookie))
        f.close()
        
    def __read_seesion(self):
        if os.path.exists('D:/million/session'):
            f=open('D:/million/session','r')
            self.__cookie=f.read().split(':')[1]
            f.close()
            self.__poster.updata_header('Cookie', self.__cookie)
            return True
        else:
            return False
        
if __name__ == '__main__':

    logfile=logger.logger()
    MA_client = Client('jp',username)
    MA_client.login(username, passwd)

    MA_client.explore()
