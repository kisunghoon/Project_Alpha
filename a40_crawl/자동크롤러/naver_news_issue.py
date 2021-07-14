import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import pymysql.cursors 
import time

crawlDate = time.strftime('%Y-%m-%d %H:%M:%S')
print('크롤링 :', crawlDate)

url = "https://www.naver.com"
response = requests.get(url)
dom = BeautifulSoup(response.text, "html.parser")
elements = dom.select("#yna_rolling .issue")

result = [
    {
        "뉴스" : element.text.strip(),
        "URL" : element.attrs['href'].strip()
    }    
    for element in elements
]

print(result)

df = pd.DataFrame([], columns=['뉴스', 'URL'])
for data in result:
    df.loc[len(df)] = data

conn = pymysql.connect(host='localhost',
        user='myuser',
        password='1234',
        database='mydb')

# prepares statement 방식
try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO NAVER_NEWS_ISSUE(news, url, crawlDate) VALUES (%s, %s, %s)'
        
        for news_issue in result:
            cursor.execute(sql, (news_issue['뉴스'], news_issue['URL'], crawlDate))

    conn.commit()
    print('DB 에 저장했습니다')

# pymysql 을 다룰때 자주 등장하는 Error 들.
except (pymysql.err.OperationalError, pymysql.ProgrammingError, 
        pymysql.InternalError, pymysql.IntegrityError) as e:
    print(e.args)
    print("mysql에러코드:", e.args[0])  # MySQL 에러코드
    print("mysql에러메세지:", e.args[1])  # MySQL 에러 메세지

finally:
    conn.close()
