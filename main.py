import hashlib
import requests
from bs4 import BeautifulSoup
from config import html_site


def top_hash_category(a: dict, hash_md5: str):
    res = {}
    for key, value in a.items():
        if hash_md5 in value:
            res[key] = res.get(key, 0) + value.count(hash_md5)
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


db = {}
with open('db.txt', 'r') as f:
    all_hash = [i.strip().split(';') for i in f.readlines()]
    for hash_md5, category in all_hash:
        db[category] = db.get(category, []) + [hash_md5]
soup = BeautifulSoup(html_site, "html.parser")
images = soup.find_all('img')
all_img = [i.get('src') for i in images if
           i.get('src') not in ['images/icons/icon-loading.png', 'images/icons/icon-refresh.png']]
category = soup.find_all('input', {'type': 'hidden', 'name': 'category'})[0].get('value')
res = []
for i in all_img:
    response = requests.get("http://www.humansnotinvited.com/" + i)
    md5_hash = hashlib.md5(response.content).hexdigest()
    print(f'{"▋" * (len(res) + 1)} - {len(res) + 1}/9')
    if top_hash_category(db, md5_hash)[0][0] == category:
        res.append('+')
    else:
        res.append('-')
print(category)
for i in range(3):
    print(' '.join(res[i * 3:(i + 1) * 3]))
