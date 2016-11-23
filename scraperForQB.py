import urllib2
import urllib
import time
import cookielib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ScraperForQB:
	def __init__(self,url,pageIndex,repeat = 2,headers = None,values = None,method = None,timeout = 100,filename = None,pattern = None):
		self.pageIndex = pageIndex
		self.url = url
		self.storage = []
		self.quit = False
		self.headers = headers
		self.values = values
		self.method = method
		self.timeout = timeout
		self.filename = filename
		self.pattern = pattern
		self.elementC = 0
		self.repeat = repeat

	def generateRequest(self,url,data,method):
		if method == 'POST':
			return urllib2.Request(url,data, headers = self.headers)
		elif method == 'GET':
			return urllib2.Request(url+'?'+data,headers = self.headers)
		else:
			return urllib2.Request(url,headers = self.headers)

	def setUp(self,url):
		httpHandler = urllib2.HTTPHandler(debuglevel = 1)
		httpsHandler = urllib2.HTTPSHandler(debuglevel = 1)
		opener = urllib2.build_opener(httpHandler,httpsHandler)
		urllib2.install_opener(opener)
		data = urllib.urlencode(self.values) if self.values else None
		return self.generateRequest(url,data = data,method = self.method)

	def getPageText(self,url):
		self.pageIndex += 1
		temp = url + str(self.pageIndex)
		print ('logging into ' + temp + '\n')
		request = self.setUp(temp)
		try:
			response = urllib2.urlopen(request,timeout = self.timeout)
		except urllib2.URLError, e:
			if hasattr(e,'code'):
				print ("Error Code: " + str(e.code))
			elif hasattr(e,'reason'):
				print ("Error Reason: " + str(e.reason))
		print ('received response, waiting for filtering \n')
		return response.read()
		

	def filterText(self,text):
		if self.pattern:
			items = re.findall(self.pattern,text)
			tempStorage = []
			for item in items:
				replaceBR = re.compile('<br/>')
				subText = re.sub(replaceBR,'\n',item[1])
				tempStorage.append([item[0].strip(),subText.strip()])
				print('----------------------------------------------')
			self.elementC = 2
			print ('finish filtering \n')
			return tempStorage
		print 'cannot filter it'
		return text

	def write(self,items,filename):
		print ('start writing to file \n')
		f = open(filename,'a')
		temp = ''
		for item in items:
			for i in range(self.elementC):
				repeat = 1 if i != self.elementC-1 else self.repeat
				temp += item[i] + '\n'*repeat
		f.write(temp)
		f.close()
		print ('finish writing')

	def printI(self,items):
		# for item in items:
		# 	print item.encode()
		pass

	def start(self):
		while not self.quit :
			cmd = raw_input('wait for your cmd...')
			if cmd == 'q' or cmd == 'Q':
				self.quit = True
			print str(cmd)
			print('start....')
			text = self.getPageText(self.url)
			items = self.filterText(text)
			if self.filename:
				self.write(items,self.filename)
			else:
				self.printI(items)
		print ('finished......')
		return None

pageIndex = 0
url= 'http://www.qiushibaike.com/hot/page/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
filename = 'C:\Users\ASUS\Desktop\workfile.txt'
pattern = re.compile('<a.*?title.*?h2>(.*?)</h2>.*?content.*?span>(.*?)</',re.S)
repeat = 3
scraber = ScraperForQB(url = url, repeat = repeat, headers = headers, pageIndex = pageIndex,filename = filename,pattern = pattern)
#scraber = ScraperForQB(url = url,headers = headers,pageIndex = 0,pattern = pattern)
scraber.start()