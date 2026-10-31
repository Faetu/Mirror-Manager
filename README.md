# Mirman
Python script to manage the mirrorlist of an arch linux machine


## Installation
Currently, the installation must be done manually
### Download
First of all you need to download the script. Its only a single .py file.


    git clone https://github.com/Faetu/Mirror-Manager.git
### Install
Now we need to make the script run able and run able from anywhere
First make the script run able:


    sudo chmod +x mirman.py
now we need to move the script to /bin


    mv ./mirror_manager.py /bin
Now the script is run able and callable from anywhere!


## How to use
This script is made to manage the mirrorlist on an arch-linux machine.
You can call: 


    mirman -h


To show all the options.
### Example
One Example can be:


    mirman -c CH DE AT -p http -b
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