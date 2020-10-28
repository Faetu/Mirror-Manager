# Mirman
Python script to manage the mirrorlist of an arch linux machine

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![release](https://img.shields.io/github/v/release/Faetu/mirror-manager.svg?include_prereleases)](https://github.com/Faetu/Mirror-Manager/releases) ![requirements](https://img.shields.io/badge/requirements-up%20to%20date-green)


## Installation
Clone the repo
```sh
git clone https://github.com/Faetu/Mirror-Manager.git
```
Change directory
```sh
cd mirror-manager
```
Run setup file with root privileges
```sh
sudo sh setup.sh
```
## How to use
This script is made to manage the mirrorlist on an arch-linux machine.
You can call: 
```sh
mirman -h
```
To show all the options.
### Example
One Example can be:
```sh
mirman -c CH DE AT -p http -b
```
`-c` `--country`
This argument will tell mirman to only request for those three countries: `CH` (Switzerland) `DE` (Germany) and `AT` (Austria).


`-p` `--protocol`
This argument will tell mirman witch protocol we wish to request.


 - http
 - https


`-b` `--backup-old-mirrorlist`
With this argument, we told mirman to make a backup file of the current mirrorlist file.
If a mirrorlist.back001 exist, then mirman create a mirrorlist.back002.(count till 999)
This option is false by default.


### Update functionality
If you have done one time a request with this script, then your mirrorlist is filled with a list of server from some countries and also with the used options for IP version and protocol.
At this moment you will be able to use the update function without trouble.


    mirman -u


This argument let mirman read your actual mirrorlist, it searches for country-tags and also for IP version and protocol. After analysis the script start his work automatically.


## What's special on this script?
Mirman has since the v1.4 the functionality to check all the domains for there server origin.
Some of the domains are for example from germany, but the server himself is located in the united state. In the end, before mirman write to the mirrorlist file, he will ask if the user accept servers. For each country he will ask separated.

Example output:

> \## Germany
 Server = http://mirror.23media.com/archlinux/$repo/os/$arch
 Server = https://mirror.23media.com/archlinux/$repo/os/$arch
 Server = https://appuals.com/archlinux/$repo/os/$arch `--> real origin: Canada`
 Server = http://artfiles.org/archlinux.org/$repo/os/$arch
 Server = http://mirror.mikrogravitation.org/archlinux/$repo/os/$arch
 Server = https://mirror.mikrogravitation.org/archlinux/$repo/os/$arch
 Server = https://ger.mirror.pkgbuild.com/$repo/os/$arch `--> real origin: unknown`
 Server = https://mirror.pkgbuild.com/$repo/os/$arch

The script will ask your premission to use urls with different origins.
