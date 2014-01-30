'''
Created on 2014-1-30

@author: bell
'''
#!C:/python27
import base64

from Crypto.Cipher import AES
import Const

class Crypter():
    
    def __init__(self,location):
        self.__location=location
        _keys=getattr(Const,'AES_KEY')[self.__location]
        self.__AES_key='%s%s' % (_keys['crypt'] , '0' * 16)
        self.__RES_key=_keys['crypt']
        self.__AES_cipher=self.__create_AES_cipher(self.__AES_key,AES.MODE_ECB)
        
    def __create_AES_cipher(self,key,mode):
        return AES.new(key,mode)
    
    def __pad(self,string):
        return string  + (16 - len(string) % 16) * chr(16 - len(string) % 16)
    
    #used to encode post data
    #plain -> AES ECB -> base64
        
    def encode_one_para(self,parameter):
        return base64.encodestring((self.__AES_cipher.encrypt(self.__pad(parameter)))).strip('\n')
    
    #decrypt data form server
    def decrypt(self,data):
        return self.__AES_cipher.decrypt(data)