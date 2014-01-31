'''
Created on 2014-1-30

@author: bell
'''
import Connecter
import Player
import Const

class Client():

    def __init__(self, location,username):

        self.__location = location
        self.__poster = Connecter.poster(location,username)
        self.__player = Player.Player(self.__poster)
    #log in
    def login(self, username, passwd):

        _postdata = {'login_id': username,
                     'password': passwd
                     }
        _url='check_inspection'
        _content, _header = self.__poster.post(_url)
        if 'Set-Cookie' in _header:
            self.__cookie = _header['Set-Cookie'].split(
                ',')[1].split(';')[0].lstrip(' ')
            self.__poster.updata_header('Cookie', self.__cookie)
        _url='login'
        _content, _header = self.__poster.post(_url
            , postdata=_postdata)
        self.__get_configure(_content)

    def __get_configure(self, _content):
        list = {'party_name':[]}
        from XMLParser import XMLParser
        #_parser = XMLParser()
        #_parser.start_parse(_content,list)
        #list = _parser.get_data(list)
    def explore(self):
        self.__player.explore()

if __name__ == '__main__':

    MA_client = Client('jp',username)
    MA_client.login(username, passwd)
    MA_client.explore()
