import re, time, sys, random, socks, socket, string
from BeautifulSoup import BeautifulSoup
from threading import Thread

#Proxy settings
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9050, True)
socket.socket = socks.socksocket

#Banner
print '''
   ____        _                _____                                 
  / __ \      (_)              / ____|                                
 | |  | |_ __  _  ___  _ __   | (___   ___ __ _ _ __  _ __   ___ _ __ 
 | |  | | '_ \| |/ _ \| '_ \   \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |__| | | | | | (_) | | | |  ____) | (_| (_| | | | | | | |  __/ |   
  \____/|_| |_|_|\___/|_| |_| |_____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                      
                                                                      
'''

import urllib2

def onionCheck(onionurl):
	try:
		response = urllib2.urlopen("http://%s.onion" % onionurl).read()
		soup = BeautifulSoup(response)
		with open("list.txt", "a") as myfile:
			myfile.write("http://"+onionurl+".onion -"+soup.title.string+"\n")
		print(onionurl+".onion ("+soup.title.string+") is UP :)")
	except urllib2.HTTPError, e:
		print onionurl+".onion is down :("
	except urllib2.URLError, e:
		print onionurl+".onion is down :("

#Check if tor is running
try:
	print "Checking if tor is running..."
	ret = urllib2.urlopen('http://www.google.com')
	#Scan mode (random, from file)
	mode		=	input("1. Random strings\n2. From file\nChoose: ")
	if mode == 1:
		global stop_now, start, threads
		stop_now 	= 	False
		start		=	0
		threads 	= 	input("Threads: ")
		class httpPost(Thread):
			def __init__(self):
				Thread.__init__(self)
				self.running = True

			def _send_http_post(self, pause=10):
				global stop_now, start
				#Http request
				start_locale=start
				start+=1
				time.sleep(random.uniform(0.1, 5))
				randomword=''.join(random.choice(string.lowercase + string.digits) for n in range(16))
				onionCheck(randomword)
				for i in range(0, 9999):
					if stop_now:
						self.running = False
						break

			def run(self):
				while self.running:
						self._send_http_post()

		def main():
			global stop_now, thread

			rthreads = []
			for i in range(threads):
				t = httpPost()
				rthreads.append(t)
				t.start()

			while len(rthreads) > 0:
				try:
					rthreads = [t.join(1) for t in rthreads if t is not None and t.isAlive()]
				except KeyboardInterrupt:
					print "\nExiting threads...\n"
					for t in rthreads:
						stop_now = True
						t.running = False

		if __name__ == "__main__":
			main()
	elif mode == 2:
		filename = raw_input("Input file: ")
		f = open("%s" % filename, "r")
		for line in f:
			randomword = line.rstrip()
			onionCheck(randomword)

except urllib2.URLError, e:
	print "You must activate Tor before running this tool!"

