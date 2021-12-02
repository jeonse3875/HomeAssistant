import requests
from bs4 import BeautifulSoup

def SearchNews(keyword, count):
    url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    news_title = [title['title'] for title in soup.find_all('a', attrs={'class':'news_tit'})]
    count = min(len(news_title),count)

    return news_title[:count]
