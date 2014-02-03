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
    def login(self,username='',passwd=''):
        self.__player.login(username or self.__username,passwd or self.__passwd)
        
    def __get_configure(self, _content):
        list = {'party_name':[]}
        from XMLParser import SAXParser
        #_parser = XMLParser()
        #_parser.start_parse(_content,list)
        #list = _parser.get_data(list)
    def explore(self):
        try:
            self.__player.explore()
        except RuntimeError:
            self.relogin()
        #self.__player.fairy()


        
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
