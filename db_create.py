import hashlib
import requests
from bs4 import BeautifulSoup


url = "http://www.humansnotinvited.com/"
for i in range(1000):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all('img')
    all_img = [i.get('src') for i in images if i.get('src') not in ['images/icons/icon-loading.png', 'images/icons/icon-refresh.png']]
    category = soup.find_all('input', {'type': 'hidden', 'name': 'category'})[0].get('value')
    with open('db.txt', 'a') as f:
        for i in all_img:
            response = requests.get(url + i)
            md5_hash = hashlib.md5(response.content).hexdigest()
            print(md5_hash)
            f.write(f'{md5_hash};{category}\n')
