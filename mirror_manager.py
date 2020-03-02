#!/sur/bin/env python3

import argparse
import requests as req
import sys
import os
from os import path
from shutil import copyfile


#Args parse
Parser = argparse.ArgumentParser(prog='mirror_manager.py',description="""Get actual country-dependet mirrorlist for an arch linux system""")
Parser.add_argument('-c', '--country', help="search for specified countrys", nargs='*')
Parser.add_argument('-p', '--protocol', help='search for specified protocols', nargs='+', default=['http','https'])
Parser.add_argument('-i', '--ip_version', help='choce between ipv4 or ipv6', default=4)
Parser.add_argument('-b', '--backup_old_mirrorlist', help='make a backupfile of the old mirrorlist file', action='store_true')
Parser.add_argument('-m', '--mirrorlist_file', help='path to the mirrorlist', default='/etc/pacman.d/mirrorlist')
Parser.add_argument('-l', '--list_of_aviable_countrys', help='show a list of aviable countrys', action='store_true')
Args = Parser.parse_args()


GREEN = "\033[0;32m"
RESET = "\033[0;0m"


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
        raise ValueError("invalid default answer: '%s'" % default)

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
    Tmplink = 'https://www.archlinux.org/mirrorlist/?country=AU&country=BE&protocol=http&protocol=https&ip_version=4'
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


def MakeBackup():
    BackNam = ''
    for i in range(1,900):
        BackNam = '{}.back{:03}'.format(Args.mirrorlist_file, i)
        if not (path.exists(BackNam)):
            copyfile(Args.mirrorlist_file, BackNam)
            print('[+] made a backup of mirrorlist file: {}'.format(BackNam))
            return True


def CheckSudo():
    if(os.getuid() == 0):
        return True
    else:
        return False


# program initial
if __name__ == '__main__':
    if (Args.list_of_aviable_countrys):
        Aviables = """
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
        print(Aviables)
        exit(0)
    if not (Args.country):
        Parser.error('No country requested, add at least one country!')
    if not CheckSudo():
        UIn = Query_yes_no('You need super user privileges to write into the mirrorlist file, stop actions?')
        if UIn:
            exit(0)
    Response = GetListFromOrigin(Args.country, Args.protocol, Args.ip_version)
    print('found some server: \n\n')
    for line in Response:
        print(line)
    UIn = Query_yes_no('\nWrite new mirrorlist to {}?'.format(Args.mirrorlist_file))
    if(UIn):
        if Args.backup_old_mirrorlist:
            MakeBackup()
        with open(Args.mirrorlist_file,'w') as f:
            for line in Response:
                f.write('{}\n'.format(line))
            print('[+] write new mirrorlist to file {}'.format(Args.mirrorlist_file))
        print('\n[+] all actions were succesfully!')
        exit(0)
    else:
        print('[!] stop action because of user input!')
        exit(0)
