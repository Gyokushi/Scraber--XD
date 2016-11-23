import urllib2
import urllib
import time
import cookielib
import re
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')
class scraperForTB:

	def __init__(self,originURL,filenames,isMainpage = False,filterMode = None,onlyOwner = True,owner = None,IOFlag = 'w+',values = None,method = None,timeout = 10,collect = False,firstFloor = False,totalPage = False):
		self.originURL = originURL
		self.headers = self.myHeaders()
		self.filenames = filenames
		self.filename = filenames[0] if len(filenames) == 1 else filenames[1]
		self.URLStorage = []
		self.IOFlag = IOFlag
		self.pattern = self.myPattern()
		self.values = values
		self.method = method
		self.timeout = timeout
		self.totalPageNum = 0
		self.title = ''
		self.owner = 0
		self.filterMode = filterMode
		self.onlyOwner = onlyOwner
		self.collect = collect
		self.isMainpage = isMainpage
		self.firstFloor = firstFloor
		self.owner = owner
		self.totalPage = totalPage

	def myPattern(self):
		pattern = {}
		infoPattern = re.compile('&quot;author&quot;:{&quot;user_id&quot;:(.*?),.*?post_no.*?:(.*?),',re.S)
		contentPattern = re.compile('post_content_.*?clearfix">(.*?)<\/div>',re.S)
		n_PagePattern = re.compile('<span class="red">(.*?)<.*?',re.S)
		title = re.compile('<title>(.*?)_.*?',re.S)
		linkFormat = re.compile('_blank">(.*?)</a>',re.S)
		pattern['infoPattern'] = infoPattern
		pattern['contentPattern'] = contentPattern
		pattern['n_PagePattern'] = n_PagePattern
		pattern['title'] = title
		pattern['linkFormat'] = linkFormat
		return pattern

	def myHeaders(self):
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = {'User-Agent': user_agent}
		return headers

	def generateRequest(self,url,data):
		print 'generating request to access' + url
		if self.method == 'POST':
			return urllib2.Request(url,data, headers = self.headers)
		elif self.method == 'GET':
			return urllib2.Request(url+'?'+data,headers = self.headers)
		else:
			return urllib2.Request(url,headers = self.headers)

	def setUp(self,url):
		httpHandler = urllib2.HTTPHandler(debuglevel = 1)
		httpsHandler = urllib2.HTTPSHandler(debuglevel = 1)
		opener = urllib2.build_opener(httpHandler,httpsHandler)
		urllib2.install_opener(opener)
		data = urlencode(self.values) if self.values else None
		print 'returning request to access' + url
		return self.generateRequest(url,data = data)

	def getMainpage(self):
		request = self.setUp(self.originURL)
		print 'logging into mainpage...'
		try:
			response = urllib2.urlopen(request,timeout = self.timeout)
		except urllib2.URLError, e:
			if hasattr(e,'code'):
				print ("Error Code: " + str(e.code))
			elif hasattr(e,'reason'):
				print ("Error Reason: " + str(e.reason))
		print ('received response from mainpage, waiting for filtering \n')
		return response.read()

	def filterText(self,text):
		infoItems = self.pattern['infoPattern'].findall(text)
		contentItems = self.pattern['contentPattern'].findall(text)
		n_PageItems = self.pattern['n_PagePattern'].findall(text)
		title = self.pattern['title'].findall(text)
		self.title = title[0]
		self.totalPageNum = n_PageItems[0]
		if not self.owner: self.owner = infoItems[0][0] 

		print ('Recieved total page number ' + str(self.totalPageNum) + '\n')
		print ('title is ' + self.title + '\n')
		print ('owner is ' + self.owner +'\n')
		tempStorage = []
		i = 0
		replaceBR = re.compile('<br>')
		replaceEnd = re.compile('&nbsp;')
		for i in range(len(infoItems)):
			add = True
			userid = infoItems[i][0]
			post_no = infoItems[i][1]
			if self.filterMode and int(post_no) not in filterMode:
				add = False
				continue
			if self.onlyOwner and userid!=self.owner: 
				add = False
				continue
			subText = re.sub(replaceBR,'\n',contentItems[i])
			subText = re.sub(replaceEnd,'',subText)
			tempStorage.append({'userid':userid,'post_no':post_no,'content':subText.strip()})
			if self.collect:
				self.collectURL(subText.strip(),int(post_no),int(userid))
			print(post_no + '  ' + userid +'----------------------------------------------')
		print ('finish filtering \n')
		return tempStorage


	def collectURL(self,content,post_no,userid):
		if post_no:
			links = self.pattern['linkFormat'].findall(content)
			for link in links:
				self.URLStorage.append(link.strip())
			print 'collecting of' + str(post_no) + ' floor' + 'finished'


	def writeToFile(self,info):
		print 'start to write to file'
		print self.filename
		f = open(self.filename,self.IOFlag)
		f.write(self.title + '\n')
		for item in info:
			f.write(unicode(item['content'],errors = 'ignore').encode('utf8',errors='ignore')+'\n')
		print 'Writing finished'
		f.close()


	def start(self):
		scMainpage = self.getMainpage()
		info = self.filterText(scMainpage)
		if self.totalPage:
			for i in range(int(self.totalPageNum)):
				x = scraperForTB(self.originURL+'&pn='+str(i),[self.filenames[0]],IOFlag = 'a',owner = self.owner)
				x.start()
		self.writeToFile(info)
		if self.isMainpage and self.collect:
			for i in range(len(self.URLStorage)):
				print i
				x = scraperForTB(self.URLStorage[i],[self.filenames[0]],IOFlag = 'a',collect = False)
				x.start()
				time.sleep(1)






#originURL = 'http://tieba.baidu.com/f?kz=589747968'
#filename = ['C:\Users\ASUS\Desktop\MSScript.txt','C:\Users\ASUS\Desktop\mySwordsman.txt']
#filename = ['C:\Users\ASUS\Desktop\MSOrScript.txt','C:\Users\ASUS\Desktop\mySwordsman.txt']
#filterMode = [2,4,5,6,7,9,10]
filename = ['C:\Users\ASUS\Desktop\MSOrScript.txt']
originURL = 'http://tieba.baidu.com/f?kz=157871378'
scraper = scraperForTB(originURL,filename,True,totalPage = True)
scraper.start()