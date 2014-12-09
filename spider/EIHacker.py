#coding:UTF-8
import urllib2,cookielib,urllib
import urlparse
import re

def findByTitle(title):

	URL = 'http://www.engineeringvillage.com/search/quick.url'

	#初始化opener
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)

	headMsg = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip,deflate,sdch',
	'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	#'Cookie':'CLIENTID=M12e8c591148f3f2ae4aMd9410178165181; SECUREID=M12e8c591148f3f2ae4aMd9310178165181-77e6f8486731a231ac45aad1ead2d993; acw=5ab318047f3f84111ab2277586614dc5403ae0d%7C%24%7C0ptuOn9X0jRqP4VghGgrKFsLjRtoR8hIPZEit4IKkXpe2sMzrwOMql%2FJd6PrZZXDVDtnzavKzLiIVcNwly4%2FkXTC3Vpa3Qql; CLIENTID=M12e8c591148f785ec34M498e10178165181; CARS_COOKIE=006100470044006900620051006F0073006E00770066006200470058004400340054005500330038006600780065007A002F006A007600710041007A0043007600590053004F003500440035007A0074004F005900340043004C007900750071006900380071002F0039006B0072002B00340055007200310055005400640039003200370037006200370042005A004B006A00530059003D; RXSESSION=4ab318047f3f84111ab2277586614dc5403ae0d; JSESSIONID=4C3DB08A80CAAD0B757CF8FC535ACB8E.B5qva5K7KtPriWGaTGTROw; AWSELB=3B37634B085144FCC6BAA38543A1E4DCC9344980811AEDF135AB966EF225F271674722708D30EF9C2A3454CAACFB7E2F4A0D0E4593AE0B406FFBC892872920B8096082E35B86B54EB1ADE396817FF5DE0D59D29502; EISESSION=1_4C3DB08A80CAAD0B757CF8FC535ACB8E.B5qva5K7KtPriWGaTGTROw; ev_dldpref=null; __utma=15402594.20011973.1412862499.1412908700.1412915900.4; __utmb=15402594.4.9.1412916172615; __utmc=15402594; __utmz=15402594.1412862499.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
	'Host':'www.engineeringvillage.com',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'
	}

	header = []
	for key,value in headMsg.items():
		elem = (key , value)
		header.append(elem)
	opener.addheaders = header
	
	#第一次请求，获取cookie
	opener.open(URL)

	#print f.read()

	#for ind, cookie in enumerate(cj):
	#	print "%d - %s" % (ind, cookie)

	print '已经进行完第一次get，获取cookie'


	postDict = {
	'CID':'searchSubmit',
	'searchtype':'Quick',
	'csrfSyncToken':'',
	'resetDataBase':'1',
	'database':'1',
	'searchWord1': title ,
	'section1':'TI',
	'boolean1':'AND',
	'searchWord2':'',
	'section2':'NO-LIMIT',
	'boolean2':'AND',
	'searchWord3':'',
	'section3':'NO-LIMIT',
	'resetvar':'1',
	'doctype':'NO-LIMIT',
	'treatmentType':'NO-LIMIT',
	'language':'NO-LIMIT',
	'yearselect':'yearrange',
	'startYear':'1969',
	'endYear':'2015',
	'stringYear':'CSY1884CST1969',
	'updatesNo':'1',
	'sort':'relevance',
	#'_sourcePage':'vBMURgG4DDnVWMYCskH10-_VEpYoCxgP2pgp04XxfpKJ_HzzHH4DTysqUMa2uZ1HSlCBRZjZPjI=',
	#'__fp':'X_ZhekGAtjKZgCy3m5oeRMdfJFn2fW0gxYJ7UILlEZbN0gSaYcUDkLQUhU2UNX6GvrmxGEv8W7TitP26hjxGV3majLOwqm4gE--6bUonZv-XESw-NLq2mRWTxPS7eYN3l9nIienRNAfFcnRJPVFscyihz-eFHTGg0_BnghFZILotWA6K_T4u-g=='
	}

	#第二次请求，获取跳转URL
	URL = "http://www.engineeringvillage.com/search/submit.url"
	postData = urllib.urlencode(postDict)
	response = opener.open(URL,postData)

	print '进行了第二次提交，获取跳转URL'
	#print response.geturl()
	#print response.getcode()

	#得到所有论文信息
	#print response.read()
	
	#获取SEARCHID
	redirectURL = response.geturl()
	parsedURL = urlparse.urlparse(redirectURL)
	params = urlparse.parse_qs(parsedURL.query,True)
	SEARCHID = params['SEARCHID'][0]
	print SEARCHID
	
	
	return parseHTML(SEARCHID)

	

def parseHTML(SEARCHID):

	#获取第一篇的detail
	#获取最后结果
	URL = 'http://www.engineeringvillage.com/search/doc/detailed.url?SEARCHID='+SEARCHID+'&pageType=quickSearch&CID=quickSearchDetailedFormat&DOCINDEX=1&database=1&format=quickSearchDetailedFormat&tagscope=&displayPagination=yes'
	html_doc = urllib2.urlopen(URL).read()

	start_str = '''<table border="0" width="100%" id="detailed">'''
	end_str = '</table>'

	start = html_doc.find(start_str)
	#trs = table.findAll('tr')
	html_doc = html_doc[start:len(html_doc)]
	html_doc = html_doc[0:html_doc.find(end_str)+8]
	
	html_doc = html_doc.replace("<h3>", "<h7>")
	html_doc = html_doc.replace("</h3>","</h7>")

	p = re.compile('<span style=\\"font-weight: normal;font-size: 14px\\">.*span>')
	html_doc = p.sub('',html_doc)

	return html_doc
	#for tr in trs:
	#	print tr
