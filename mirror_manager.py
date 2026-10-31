import argparse
import requests as req

#Args parse
parser = argparse.ArgumentParser(prog='mirror_manager.py',description="""Show all mirroer configs!""")
parser.add_argument('-c', '--country', help="search for specified country")
parser.add_argument('-e', '--only_enabled', action='store_true',help="Show only enabled servers!", default=False)
args = parser.parse_args()


GREEN = "\033[0;32m"
RESET = "\033[0;0m"

class ArchLinuxOrg():
    def __init__(self, countrys, protocols, ip_version):
        tmplink = 'https://www.archlinux.org/mirrorlist/?country=AU&country=BE&protocol=http&protocol=https&ip_version=4'
        link = 'https://www.archlinux.org/mirrorlist/?'
        if type(countrys) is list:
            print("got list!")
        myList = req.get(tmplink)
        print(myList.text)

ArchLinuxOrg('AU','http',4)

class Server():
    def __init__(self, status, path):
        self.status = status
        self.path = path

class Country():
    def __init__(self, nation_name):
        self.myServList = []
        self.nation_name = nation_name
    def addServer(self, status, path):
        self.myServList.append(Server(status, path))
    def showAllServerStatus(self):
        print("\n---> "+self.nation_name)
        for server in self.myServList:
            if(server.status):
                print(GREEN+"[+] "+server.path+RESET)
            else:
                if(args.only_enabled is not True):
                    print("[-] "+server.path)

mirrorlist = []
myCountrys = []
with open('/etc/pacman.d/mirrorlist') as f:
    for line in f:
        mirrorlist.append(line)

for i in range(3,len(mirrorlist)):
    if("## " in mirrorlist[i]):
        tmpCountry = Country(mirrorlist[i][3:].replace("\n", ""))
        for a in range(i+1, len(mirrorlist)):
            if(mirrorlist[a] != "\n"):
                if(mirrorlist[a][0] == "#"):
                    tmpCountry.addServer(False, mirrorlist[a][1:].replace("\n", ""))
                else:
                    tmpCountry.addServer(True, mirrorlist[a].replace("\n", ""))
            else:
                myCountrys.append(tmpCountry)
                i = a
                break

for country in myCountrys:
    if(args.country != None):
        if(country.nation_name.lower() == args.country.lower()):
            country.showAllServerStatus()
    else:
        country.showAllServerStatus()
