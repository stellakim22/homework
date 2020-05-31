import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
geniemusic = soup.select('#body-content > div.newest-list > div > table > tbody > tr')


for genie in geniemusic:
    a_tag = genie.select_one('td.info > a.title')
    
    if a_tag is not None:
        rank = genie.select_one('td.number').text.split(' ')[0].rstrip()
        title = a_tag.text.rstrip().lstrip()
        artist = genie.select_one('td.info > a.artist').text.rstrip()
        print(rank, title, artist)


        db.genie.insert_one({"rank":rank, "title": title, "artist": artist})