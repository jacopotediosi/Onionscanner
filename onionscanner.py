import re, time, sys, random, socks, socket, string
from BeautifulSoup import BeautifulSoup
from threading import Thread

#Proxy settings
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9050, True)
socket.socket = socks.socksocket
def getaddrinfo(*args):
	return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

#Styling
class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   END = '\033[0m'

#Banner
print '''
   __ _        _                _____                                 
  / __ \____  (_)___  ____     / ___/_________ _____  ____  ___  _____
 / / / / __ \/ / __ \/ __ \    \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
/ /_/ / / / / / /_/ / / / /   ___/ / /__/ /_/ / / / / / / /  __/ /    
\____/_/ /_/_/\____/_/ /_/   /____/\___/\__,_/_/ /_/_/ /_/\___/_/                                                                      
'''

import urllib2

#Request
def onionCheck(onionurl):
	try:
		response = urllib2.urlopen("http://%s.onion" % onionurl).read()
		soup = BeautifulSoup(response)
		try:
			with open("list.txt", "a") as myfile:
				myfile.write("http://"+onionurl+".onion - "+soup.title.string+"\n")
			sys.stdout.write( color.BOLD + "[+] http://"+onionurl+".onion - "+soup.title.string+" is UP :)" + color.END + "\n" )
		except:
			with open("list.txt", "a") as myfile:
				myfile.write("http://"+onionurl+".onion - No title\n")
			sys.stdout.write( color.BOLD + "[+] http://"+onionurl+".onion - No title is UP :)" + color.END + "\n" )
	except urllib2.HTTPError, e:
		sys.stdout.write( color.RED + "[+] http://"+onionurl+".onion is down :(" + color.END + "\n" )
	except urllib2.URLError, e:
		sys.stdout.write( color.RED + "[+] http://"+onionurl+".onion is down :(" + color.END + "\n" )

#Check if tor is running
try:
	print "Checking if tor is running..."
	ret = urllib2.urlopen('http://www.google.com')
	#Scan mode (random, from file)
	mode = input("1. Random strings\n2. From file\nChoose: ")
	if mode == 1:
		threads = input("Threads: ")
		class newThread(Thread):
			def __init__(self):
				Thread.__init__(self)
				self.daemon = True
				self.start()
			def run(self):
				while True:
					#Http request
					randomword=''.join(random.choice(string.lowercase + string.digits) for n in range(16))
					onionCheck(randomword)
		for nt in range(threads):
			newThread()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			sys.stdout.write( color.BOLD + "\n[+] Exiting ...\n" + color.END + "\n" )
	elif mode == 2:
		filename = raw_input("Input file: ")
		f = open("%s" % filename, "r")
		for line in f:
			randomword = line.rstrip()
			onionCheck(randomword)
	else:
		sys.stdout.write( color.BOLD + "[+] Insert 1 or 2, exiting...\n" + color.END + "\n" )

except urllib2.URLError, e:
	sys.stdout.write( color.BOLD + "[+] You must activate Tor before running this tool!\n" + color.END + "\n" )

