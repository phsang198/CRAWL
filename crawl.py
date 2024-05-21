import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://baomoi.com/'

response = requests.get(url)
web_content = response.content

soup = BeautifulSoup(web_content, 'html.parser')

links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href == "https://baomoi-static.bmcdn.me/web/styles/fonts/text-font/2.0.2/styles.css":
        a = 0
    if href:
        parsed_href = urlparse(href)
        # Kiểm tra xem liên kết có phải là liên kết cấp 1 hay không
        if parsed_href.scheme and parsed_href.netloc:
            print(href)
