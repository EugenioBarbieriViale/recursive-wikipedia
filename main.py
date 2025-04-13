import requests
import time
from random import randint
from bs4 import BeautifulSoup, SoupStrainer

url = "https://en.wikipedia.org"
rand_url = "http://en.wikipedia.org/wiki/Special:Random"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Help" in s)

def attempt(limit, query="", i=0):
    s = requests.Session()
    s.cookies["news.lang"] = "en"

    if i == 0:
        r = s.get(rand_url, headers=headers)
    else:
        r = s.get(url + query, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser", parse_only=SoupStrainer('p'))

    for link in soup.find_all("a"):
        new_query = link.get("href")
        if new_query[0:6] == "/wiki/" and condition(new_query):
            break

    print(i, new_query)
    i += 1

    if i < limit and (new_query != "/wiki/Philosophy" or new_query != "/wiki/Philosophical":
        time.sleep(1)
        return attempt(limit, new_query, i)

    elif i >= limit:
        print("NOT FOUND")
        return 1

    else:
        print("-------------------")
        print("FOUND AFTER", i, "ATTEMPTS")
        return 0

n = 10
m = 0

for i in range(n):
    if attempt(20) == 0:
        m += 1

print("\n Rate:", m/n*100, "%")
