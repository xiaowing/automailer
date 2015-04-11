#!/usr/bin/env python  
#coding: utf-8

import smtplib
import sys, getopt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from confreader import MailfigReader

class MailSender:
    
    def __init__(self, host, user, user_addr, pwd):
        at_index = user_addr.find('@')
        if (at_index == -1):
            raise Exception("Incorrect user address.")
        self.__user = user
        self.__addr = user_addr
        self.__host = host
        self.__pwd = pwd
    
    def SendAllOnce(self, recv_dict, fmttext):
        if not isinstance(recv_dict, dict):
            raise Exception("Incorrect parameter type.")
        
        msg = self.__createMIMEmsg(recv_dict, fmttext)
        if msg:
            self.__send2one(msg)
    
    def SendAllRespective(self, recv_dict, fmttext):
        if not isinstance(recv_dict, dict):
            raise Exception("Incorrect parameter type.")
        
        for k, v in recv_dict.items():
            msg = self.__createMIMEmsg({k:v}, fmttext)
            if msg:
                self.__send2one(msg)

    def __send2one(self, msg):
        # http://blog.csdn.net/bravezhe/article/details/7659198
        if not isinstance(msg, MIMEMultipart):
            raise Exception("Incorrect parameter type.")

        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.__host)
            smtp.login(self.__user, self.__pwd)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.quit()
        except smtplib.SMTPException as e:
            print(str(e))

    
    def __createMIMEmsg(self, recv_dict, fmttext):
        subject = fmttext[0]
        content = fmttext[1]
        '''msg = MIMEText(self.__embedreceiver(name, content))'''
        
        if not isinstance(recv_dict, dict):
            raise Exception("Incorrect parameter type.")
            
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.__user+"<"+self.__addr+">"
        
        if len(recv_dict) > 1:
            to_addr = ';'.join(list(recv_dict.keys()))
        elif len(recv_dict) == 1:
            to_addr = list(recv_dict.keys())[0]
        else:
            raise Exception("Empty dictionary keys")
        msg['To'] = to_addr
        
        name = ''
        if len(recv_dict) > 1:
            i = 0
            for value in list(recv_dict.values()):
                if value.strip():
                    name += (value + ',')
                i += 1
                if i % 5 == 0:
                    name += '\n'
            pos = name.rfind(',')
            name = name[:pos]
            name += ':'
        elif len(recv_dict) == 1:
            name = list(recv_dict.values())[0]
            if not name.strip():
                name += ':'
        else:
            raise Exception("Empty dictionary values")
        
        txt = MIMEText(self.__embedreceiver(name, content))
        msg.attach(txt)
        
        # TODO: attachment
        return msg

    def __embedreceiver(self, name, mailcontxt):
        return str(mailcontxt %name)

def usage():
    print ("usage: python automailer -i configfile -f mailtxt [-a attachment] [-r | --respectively]")

def main(argv):
    if len(argv) < 5 or len(argv) > 8:
        print("Invalid arguments.")
        usage()
        sys.exit(1)
        
    format_string = ("i:f:r", "i:f:a:r")
    
    try:
        if "-a" in argv:
            opts, args = getopt.getopt(sys.argv[1:], format_string[1], ["respectively"])
        else:
            opts, args = getopt.getopt(sys.argv[1:], format_string[0], ["respectively"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    resflag = False    
    for op, value in opts:
        if op == "-i":
            configpath = value
        elif op == "-f":
            txtfilepath = value
        elif op == "-a":
            attachpath = value
        elif op in ['-r', '--respectively']:
            resflag = True
        else:
            print(str("Unrecognised option."))
            usage()
            sys.exit(3)
    
    
    # sender = MailSender(smtpserver, useraddr, password)
    configReader = MailfigReader(configpath, txtfilepath)
    
    from_dict = configReader.GetFromDict()
    smtpserver = from_dict[MailfigReader.KEY_SMTPSV]
    username = from_dict[MailfigReader.KEY_USRNAME]
    mailaddr = from_dict[MailfigReader.KEY_USRADDR]
    password = from_dict[MailfigReader.KEY_USRPWD]
    sender = MailSender(smtpserver, username, mailaddr, password)
    
    to_dict = configReader.GetToDict()
    fmttext = configReader.GetFmtText()
    
    if resflag:
        sender.SendAllRespective(to_dict, fmttext)
    else:
        sender.SendAllOnce(to_dict, fmttext)
    
    sys.exit(0)
    
if __name__=='__main__':
    main(sys.argv)
    

