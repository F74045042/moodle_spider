import requests
import getpass
import time
from bs4 import BeautifulSoup

# Login information
USERNAME = str(input('Student_ID: '))
PASSWORD = str(getpass.getpass('Password: '))
LOGIN_URL = 'http://moodle.ncku.edu.tw/login/'
###

# Target URL
URL = str(input('Target_URL: ') + '&view=4')
###

# Get request and find login token
print('=========================')
print('Initialization.... ', end='')
session_requests = requests.Session()
res = session_requests.get(LOGIN_URL)
soup = BeautifulSoup(res.text, "html.parser")
print('OK')
print('GET login_token.... ', end='')
TOKEN = soup.find('input', {'name':'logintoken'})['value']
print('OK')
###

# Header and data for POST
headers = {
	'Host': 'moodle.ncku.edu.tw',
	'Connection': 'keep-alive',
	'Content-Length': '83',
	'Cache-Control': 'max-age=0',
	'Origin': 'https://moodle.ncku.edu.tw',
	'Upgrade-Insecure-Requests': '1',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'Referer': LOGIN_URL,
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

payload = {
	'username': USERNAME,
	'password': PASSWORD,
	'logintoken': TOKEN
}
###

# POST request(login moodle)
print('POST the requests... ', end='')
res = session_requests.post(LOGIN_URL, data = payload, headers = headers)
###

# GET request if login successfully
soup = BeautifulSoup(res.text, "html.parser")
if(soup.find("div", attrs={"class": "logininfo"}).text == "您尚未登入。"):
	print('FAIL')
else:
	print('OK')
	print('GET the requests... ', end='')
	res = session_requests.get(URL)
	print('OK')
	print('=========================')
	# Show student name
	soup = BeautifulSoup(res.text, "html.parser")
	print('Student: [' + soup.h2.text + ']')
###
	# every 20sec scan the web again
	num = 1
	while True:
		table = soup.findAll("table", attrs={"class":"generaltable attwidth boxaligncenter"})
		tab = table[0]
		for tr in tab.tbody.findAll('tr'):
			print('=========', num,'=========')
			for td in tr.findAll('td'):
				print(td.text)
		print('==================')
		for i in range(20, 0, -1):
			print('Loading.... ', i, 'sec'.ljust(4), end='\r', flush=True)
			time.sleep(1)
		res = session_requests.get(URL, headers = dict(referer = URL))
		soup = BeautifulSoup(res.text, "html.parser")

		num += 1
	###

res.close()