#!/usr/bin/env python  
#coding: utf-8

import os.path
import configparser

class MailfigReader(object):
    __SECTION_RECEIVER = 'receiver'
    __SECTION_SENDER = 'sender'
    __SECTION_MAILTXT = 'mailtext'
    KEY_SMTPSV = 'smtp'
    KEY_USRNAME = 'user'
    KEY_USRADDR = 'address'
    KEY_USRPWD = 'password'
    __KEY_SUBJECT = 'subject'
    
    def __init__(self, inipath, txtpath):
        if not isinstance(inipath, str):
            raise Exception("Incorrect user address.")
        
        if not isinstance(txtpath, str):
            raise Exception("Incorrect user address.")
        
        
        if not os.path.isfile(inipath):
            raise Exception("Invalid config file.")
        
        if not os.path.isfile(txtpath):
            raise Exception("Invalid config file.")
        
        # TODO: character encoding
        self.__config = configparser.ConfigParser()
        self.__config.read(inipath)
        self.__txtfle = open(txtpath)
        
    def GetFromDict(self):
        from_dict = dict()
        if MailfigReader.__SECTION_SENDER in self.__config:
            for k,v in self.__config[MailfigReader.__SECTION_SENDER].items():
                if(k in [MailfigReader.KEY_SMTPSV, MailfigReader.KEY_USRNAME, 
                         MailfigReader.KEY_USRADDR, MailfigReader.KEY_USRPWD]):
                    from_dict[k] = v
        if len(from_dict) != 4:
            self.__txtfle.close()
            raise Exception("Invalid config file content.")
        
        return from_dict
    
    def GetToDict(self):
        to_dict = dict()
        
        if MailfigReader.__SECTION_RECEIVER in self.__config:
            for k,v in self.__config[MailfigReader.__SECTION_RECEIVER].items():
                to_dict[k] = v
        
        return to_dict
    
    def GetFmtText(self):
        fmttxt = list()
        
        if MailfigReader.__SECTION_MAILTXT in self.__config:
            try:
                fmttxt.append(str(self.__config[MailfigReader.__SECTION_MAILTXT][MailfigReader.__KEY_SUBJECT]))
            except configparser.NoOptionError as e:
                self.__txtfle.close()
                raise Exception(e)          
        
        try:
            mailtxt = self.__txtfle.read()
            fmttxt.append(mailtxt)
        except IOError as ex:
            raise Exception(ex)
        finally:
            self.__txtfle.close()
            
        return fmttxt
