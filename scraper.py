import urllib2
import urllib
import time
import cookielib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')



def generateRequest(url,data,method):
	if method == 'POST':
		return urllib2.Request(url,data, headers = generateHeader(user_agent))
	elif method == 'GET':
		return urllib2.Request(url+'?'+data, headers = generateHeader(user_agent))
	else:
		return urllib2.Request(url,headers = generateHeader(user_agent))

def generateHeader(user_agent):
	return {'User-Agent': user_agent,'cookie':cookie}

def scrabByValue(values,url,method):
	#encapsulate
	httpHandler = urllib2.HTTPHandler(debuglevel = 1)
	httpsHandler = urllib2.HTTPSHandler(debuglevel = 1)
	opener = urllib2.build_opener(httpHandler,httpsHandler)
	urllib2.install_opener(opener)
	if values:
	 data = urllib.urlencode(values) 
	else:
	 data = None
	request = generateRequest(url,data,method)
	#scrab
	print ('logging in....')
	try:
		response = urllib2.urlopen(request,timeout = timeout)
	except urllib2.URLError, e:
		if hasattr(e,'code'):
			print ("Error Code: " + str(e.code))
		elif hasattr(e,'reason'):
			print ("Error Reason: " + str(e.reason))
	else:
		text = response.read()
		print (text)
		# pattern = re.compile('<a.*?title.*?h2>(.*?)</h2>.*?content.*?span>(.*?)</',re.S)
		# items = re.findall(pattern,text)
		# f = open('C:\Users\ASUS\Desktop\workfile.txt', 'a')
		# for i in items:
		# 	k = i[0]
		# 	k += '\n'
		# 	k += i[1]
		# 	k += '\n\n'
		# 	f.write(k)


def checkCookie(url,filename = '',flag = False):

	cookie = cookielib.MozillaCookieJar(filename) if flag else cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	if flag: cookie.save(ignore_discard = True, ignore_expires = True)
	# for item in cookie:
	# 	print ('Name = '+ str(item.name))
	# 	print ('Value = ' + str(item.value))

def scrabByCookie(url,filename):
	cookie = cookielib.MozillaCookieJar(filename)
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	print(response.read())








# prepare data
url = "http://www.weibo.com/610422688/home?wvr=5"
#url = "http://www.weibo.com/yangmiblog"
#url = "http://www.weibo.com/610422688?is_all=1"
#url = 'http://buelearning.hkbu.edu.hk/login/index.php'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# name = raw_input("username: \n")
# psw = raw_input("password: \n")
# timeout = raw_input("input timeout: \n")
cookie = 'SINAGLOBAL=5736585859594.008.1464361899268; __gads=ID=d154ea9392ea5e07:T=1465374263:S=ALNI_MZGfdk59NiZOR9OVZWp-ODQy-IAkQ; _s_tentry=login.sina.com.cn; Apache=2786212093969.1226.1479461740125; ULV=1479461740145:43:8:1:2786212093969.1226.1479461740125:1478674227811; login_sid_t=f6c48ac6615b0c0cd4bf580efa27d0a9; UOR=v.baidu.com,widget.weibo.com,cuiqingcai.com; appkey=; SCF=AuvTwgDUtLxMM8olsLNXJiq8OFwatxgowM-uTjMZa6_M7b6g2nPfEEFvcd11DkaokW3yN3XAGNwAj8mp73MVqh4.; SUB=_2A251NHOVDeTxGedH71oQ8ibMzTuIHXVWQOJdrDV8PUNbmtBeLW_mkW-iBGqngpAYACRDHctzC2gvA9jHyw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPTu1QRoUiqpTQQHiT7N-_5JpX5KzhUgL.Fo24Shnpeon7SoM2dJLoIEBLxK-LBK2L1KBLxKqL1KqLB-qLxK.L1KzL1h.LxK-LB-BL1K5t; SUHB=079ikdeLw-4EG5; ALF=1511077701; SSOLoginState=1479541702; wvr=6'
name = 14253100
psw = 'boxmelon911A.'
timeout = 10
values = {"username":name,"password": psw}
filename = 'cookie.txt'

# count time
millis = time.time()


#checkCookie(url,filename,True)
#scrabByValue(values,url,'POST')
scrabByValue(None,url,None)
#scrabByCookie(url,filename)

print ('finished in '+str(time.time()-millis)+' s')

