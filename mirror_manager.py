#!/usr/bin/env python3

import argparse
import requests as req
import socket
import sys
import os
from os import path
from shutil import copyfile


#Args parse
Parser = argparse.ArgumentParser(prog='mirman',description="""Get actual country-dependet mirrorlist for an arch linux system""", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
Parser.add_argument('-c', '--country', help="search for specified countrys", nargs='+')
Parser.add_argument('-p', '--protocol', help='search for specified protocols', nargs='+', default=['http','https'],)
Parser.add_argument('-i', '--ip-version', help='choce between ipv4 or ipv6', default=4)
Parser.add_argument('-b', '--backup-old-mirrorlist', help='make a backupfile of the old mirrorlist file', action='store_true')
Parser.add_argument('-m', '--mirrorlist-file', help='path to the mirrorlist', default='/etc/pacman.d/mirrorlist')
Parser.add_argument('-l', '--list-of-available-countrys', help='show a list of available countrys', action='store_true')
Parser.add_argument('-u', '--update', help='update mirrorlist based on the existing countrys, protocols and ip version', action='store_true')
Parser.add_argument('-w', '--without-origin-check', help='disable origin check for server domain', action='store_true')
Parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.3')
Args = Parser.parse_args()
ip_version = getattr(Args, 'ip_version')
backup_old_mirrorlist = getattr(Args, 'backup_old_mirrorlist')
mirrorlist_file = getattr(Args, 'mirrorlist_file')
list_of_available_countrys = getattr(Args, 'list_of_available_countrys')
without_origin_check = getattr(Args, 'without_origin_check')

Availables = """
all All
AU Australia
AT Austria
BD Bangladesh
BY Belarus
BE Belgium
BA Bosnia and Herzegovina
BR Brazil
BG Bulgaria
CA Canada
CL Chile
CN China
CO Colombia
HR Croatia
CZ Czechia
DK Denmark
EC Ecuador
FI Finland
FR France
GE Georgia
DE Germany
GR Greece
HK Hong Kong
HU Hungary
IS Iceland
IN India
ID Indonesia
IR Iran
IE Ireland
IL Israel
IT Italy
JP Japan
KZ Kazakhstan
KE Kenya
LV Latvia
LT Lithuania
LU Luxembourg
NL Netherlands
NC New Caledonia
NZ New Zealand
MK North Macedonia
NO Norway
PY Paraguay
PH Philippines
PL Poland
PT Portugal
RO Romania
RU Russia
RS Serbia
SG Singapore
SK Slovakia
SI Slovenia
ZA South Africa
KR South Korea
ES Spain
SE Sweden
CH Switzerland
TW Taiwan
TH Thailand
TR Turkey
UA Ukraine
GB United Kingdom
US United States
VN Vietnam
        """
BLINK = "\033[5m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '{}\033[93m'.format(BLINK)
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
POSITIV = "{}[+] ".format(OKGREEN)
NEGATIV = "{}[!] ".format(FAIL)

def Print_Warning(text):
    print("{}{}{}".format(WARNING,text,RESET))

def Print_Error(text):
    print("{}{}{}".format(NEGATIV, text, RESET))

def Print_Sucess(text):
    print("{}{}".format(POSITIV, text))

def RemoveLastLine():
    sys.stdout.write("\033[F") #back to previous line
    sys.stdout.write("\033[K") #clear line

# got this from https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def Query_yes_no(Question, Default="yes"):
    Valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if Default is None:
        Prompt = " [y/n] "
    elif Default == "yes":
        Prompt = " [Y/n] "
    elif Default == "no":
        Prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % Default)

    while True:
        sys.stdout.write(Question + Prompt)
        Choice = input().lower()
        if Default is not None and Choice == '':
            return Valid[Default]
        elif Choice in Valid:
            return Valid[Choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def GetListFromOrigin(Countrys, Protocols, Ip_version):
    CountryTag = ''
    if type(Countrys) is list:
        for c in Countrys:
            CountryTag += 'country={}&'.format(c)
    else:
        CountryTag = 'country={}&'.format(Countrys)

    ProtocolTag = ''
    if type(Protocols) is list:
        for p in Protocols:
            ProtocolTag += 'protocol={}&'.format(p)
    else:
        ProtocolTag = 'protocol={}&'.format(Protocols)
    Link = 'https://www.archlinux.org/mirrorlist/?{}{}ip_version={}'.format(CountryTag, ProtocolTag, Ip_version)
    Awnser = req.get(Link)
    ActiveList = []
    for line in Awnser.text.split('\n'):
        if(line[0:2] == '#S'):
            ActiveList.append(line[1:])
        else:
            ActiveList.append(line)
    return ActiveList


def OriginCheck(ServerDomain, Origin):
    if('http://' in ServerDomain):
        ServerDomain = ServerDomain[7:]
    elif('https://' in ServerDomain):
        ServerDomain = ServerDomain[8:]
    EndOfRegularURL = ServerDomain.find('/')
    if(EndOfRegularURL > -1):
        ServerDomain = ServerDomain[:EndOfRegularURL]
    HostIP = socket.gethostbyname(ServerDomain)
    RequestOrigin = req.get('http://api.db-ip.com/v2/free/'+HostIP+'/countryName')
    RealOrigin = RequestOrigin.text
    if(RealOrigin == Origin):
        return '-1'
    else:
        return RealOrigin


def MakeBackup():
    BackNam = ''
    for i in range(1,900):
        BackNam = '{}.back{:03}'.format(Args.mirrorlist_file, i)
        if not (path.exists(BackNam)):
            copyfile(Args.mirrorlist_file, BackNam)
            Print_Sucess('made a backup of mirrorlist file: {}'.format(BackNam))
            return True


def CheckSudo():
    if(os.getuid() == 0):
        return True
    else:
        return False


def NotAllowedOrigin(List, Line):
    for o in List:
        for l in o.ServerList:
            if(l == Line):
                return True
    return False


class SuspectOrigins():
    def __init__(self, ServerOrigin):
        self.ServerOrigin = ServerOrigin
        self.ServerList = []


# program initial
if __name__ == '__main__':
    if (Args.list_of_available_countrys):
        print(Availables)
        exit(0)
    if not(Args.country):
        Print_Error('to few arguments!')
        exit(0)
    if not CheckSudo():
        UIn = Query_yes_no('{}You need super user privileges to write into the mirrorlist file, stop actions?{}'.format(WARNING, RESET))
        if (UIn):
            RemoveLastLine()
            Print_Error('stop action because of user input!')
            exit(0)
    Response = GetListFromOrigin(Args.country, Args.protocol, Args.ip_version)
    print('found some server: \n\n')
    ActualCountry = ''
    SuspectOriginList = []
    for line in Response:
        if("#" in line):
            print("{}{}{}".format(HEADER, line, RESET))
            if('##' in line and len(line) > 3 and not 'Arch Linux' in line and not 'Generated' in line):
                ActualCountry = line[3:]                 
        else:
            if (not without_origin_check and 'Server' in line):
                RealOrigin = OriginCheck(line[9:], ActualCountry)
                if not(RealOrigin == '-1'):
                    if(len(SuspectOriginList) > 0):
                        for i in range(0, len(SuspectOriginList), 1):
                            if(SuspectOriginList[i].ServerOrigin == RealOrigin):
                                SuspectOriginList[i].ServerList.append(line)
                                break
                            if(i == (len(SuspectOriginList)-1)):
                                SuspectOriginList.append(SuspectOrigins(RealOrigin))
                                SuspectOriginList[i+1].ServerList.append(line)
                    else:
                        SuspectOriginList.append(SuspectOrigins(RealOrigin))
                        SuspectOriginList[0].ServerList.append(line)
                    print("{}{} --> real origin: {}{}".format(line, WARNING, RealOrigin, RESET))
                else:
                    print(line)
            else:
                print(line)
    if(not without_origin_check and len(SuspectOriginList) > 0):
        for s in range(0,len(SuspectOriginList),1):
            UIn = Query_yes_no('\nAllow domains from {} server?'.format(SuspectOriginList[s].ServerOrigin))
            if(UIn):
                print('{}Allowed origin: {}{}'.format(POSITIV, SuspectOriginList[s].ServerOrigin, RESET))
                SuspectOriginList.pop(s)
            else:
                print('{}Not allowed origin: {}{}'.format(NEGATIV, SuspectOriginList[s].ServerOrigin, RESET))
    UIn = Query_yes_no('\nWrite new mirrorlist to {}?'.format(Args.mirrorlist_file))
    if(UIn):
        if Args.backup_old_mirrorlist:
            MakeBackup()
        with open(Args.mirrorlist_file,'w') as f:
            for line in Response:
                if(not without_origin_check and NotAllowedOrigin(SuspectOriginList, line)):
                    continue
                else:
                    f.write('{}\n'.format(line))
            Print_Sucess('write new mirrorlist to file {}'.format(Args.mirrorlist_file))
        Print_Sucess('all actions were succesfully!')
        exit(0)
    else:
        Print_Error('stop action because of user input!')
        exit(0)
