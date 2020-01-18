#!/usr/bin/ python
# coding: utf-8

from webbot import Browser
import time
import mechanize
import re
import sys
from urllib.request import urlopen
import json
import getpass
import urllib
import os
"""
ref:
    https://stackoverflow.com/questions/53546836/attributeerror-list-object-has-no-attribute-decode
    https://docs.python.org/3.0/howto/urllib2.html#number-1
"""
class WebpageZte():
    RED 	= '\033[34m'
    GREEN 	= '\033[32m'
    GREEN1 	= '\033[31m' #red
    RESET 	= '\033[0;0m'

    def __init__(self,username ="",password =""):
        self.username = username
        self.password = password
    
    def LoginShodan(self):
        sys.stdout.write("\r[*]Trying Shodan login")
        sys.stdout.flush()    
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders= [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Ubuntu/3.0.1-1.fc9 Firefox/3.0.1' ) ] 
        self.browserLogin = self.browser.open("https://account.shodan.io/login")
        self.browser.select_form(nr = 0)
        self.browser["username"] = self.username
        self.browser["password"] = self.password
        self.browserClick = self.browser.submit()
        time.sleep(2)
        if self.alertLoginAccount() :
            sys.stdout.write("                  ["+WebpageZte.GREEN1+"Wrong Username or Password " +WebpageZte.RESET+"]\n")
            sys.exit(1)
        elif self.LimitAlert() :
            sys.stdout.write("                  ["+WebpageZte.GREEN1+"Login Succes " +WebpageZte.RESET+"]-->")
            sys.stdout.write("["+WebpageZte.GREEN1+"Limit API search Daily" +WebpageZte.RESET+"]\n")
            sys.exit(1)
        else:
            sys.stdout.write("                  ["+WebpageZte.GREEN+"Login Succes Ready Find Target " +WebpageZte.RESET+"]\n")

    def alertLoginAccount(self):
        self.browserRequest = self.browser.open("https://www.shodan.io/search?query=zte+country%3Aid")
        self.checkAccount = '\n'.join(self.z.decode('utf-8', 'ignore') for self.z in self.browserRequest)
        self.Bools = '<p>Daily search usage limit reached. Please create a free account to do more searches.</p>' in self.checkAccount
        return self.Bools
    
    def LimitAlert(self):
        self.limitAPI = self.browser.open("https://www.shodan.io/search?query=zte+country%3Aid")
        self.checkLimit = '\n'.join(self.z.decode('utf-8', 'ignore') for self.z in self.limitAPI)
        self.Bools = '<p>Daily search usage limit reached. Please wait a bit before doing more searches or use the API.</p>' in self.checkLimit
        return self.Bools
        
    def FindingTarget(self,url):
        self.url = url
        self.shodanSearch = self.browser.open(self.url)
        self.resultFind = self.shodanSearch.read()
        sys.stdout.write("\r[*]Try to get the target IP")
        sys.stdout.flush()
        self.hostTargets = re.findall(r'<div class="ip"><a href="/host/(.*?)">', str(self.resultFind)) 

        try:
            if self.hostTargets:
                time.sleep(1)
                sys.stdout.write("                  ["+WebpageZte.GREEN+"OK" +WebpageZte.RESET+"]-->")
                sys.stdout.write("["+WebpageZte.GREEN+"Found Target" +WebpageZte.RESET+"]\n")
                self.PrintHost()
        except:
            sys.stdout.write("["+WebpageZte.RED+"Target Not Found"+WebpageZte.RESET+"]\n")
            sys.exit()
            
    def PrintHost(self):
        for self.hostTarget in range(0,len(self.hostTargets)):
            self.Geolocation(self.hostTargets[self.hostTarget])

    def Geolocation(self,hosttarget):
        self.geolocationTarget = hosttarget
        self.url = urlopen("http://ipinfo.io/" + self.geolocationTarget + "/json")
        self.result = json.loads(self.url.read())
        sys.stdout.write("\t[+]"+WebpageZte.RED+"City:"+WebpageZte.GREEN+str(self.result['city'])+WebpageZte.RED+"\tRegion:"+WebpageZte.GREEN+str(self.result['region'])+WebpageZte.RED+"\tCountry:"+WebpageZte.GREEN+str(self.result['country'])+" "+WebpageZte.RESET+"\n")
        sys.stdout.write("\t      |_ "+WebpageZte.RED+"Location: "+WebpageZte.GREEN+str(self.result['loc'])+WebpageZte.RESET+" \n")
        sys.stdout.write("\t         |_"+WebpageZte.RED+"IP: "+WebpageZte.GREEN+str(self.hostTargets[self.hostTarget]+WebpageZte.RESET+"-->"))
        self.GetCodeResponse(self.geolocationTarget)

    def GetCodeResponse(self,hosts):
        self.hosts = hosts
        try:
            self.codeResponse = urllib.request.urlopen("http://"+str(self.hosts))
        except urllib.error.HTTPError as e:
            print(e.code)

        except urllib.error.URLError as e:
            print(e.reason)
        else:
            print("[OK "+str(self.codeResponse.code)+ "] Request fulfilled")


os.system("clear")
usrname = input("Username: ")
psswd = getpass.getpass("Password: ")
login = WebpageZte(usrname,psswd)

planTarget = int(input("Input many search: "))
tempUserInput = []

for i in range(0,planTarget):
    userInput = input("Input Target: ")
    tempUserInput.append(userInput)

login.LoginShodan()

for x in range(0,len(tempUserInput)):
    url="https://www.shodan.io/search?query={link}+country%3Aid&language=en".format(link = tempUserInput[x])
    print('\n')
    print("{page}".format(page = tempUserInput[x]).center(70,"=").upper())
    login.FindingTarget(url)
