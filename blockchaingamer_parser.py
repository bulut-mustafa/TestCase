import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import re
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a blockchaingamer.biz article.
    """
    print(url)
    soup = BeautifulSoup(html_content, "html.parser")
    site_name  = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
    author = soup.find(name='meta', attrs={'name': 'author'})
    print(author)
    published_date = soup.find(name='meta', attrs={'name': 'article:published_time'}).get('content')
    updated_date = soup.find(name='meta', attrs={'name': 'article:modified_time'}).get('content')

       
    result = {
        "url": url_content,
        "author": author,
        "published": published_date,
        "latestUpdate": updated_date,
        'siteName': site_name
    }
    return result
with open("dataset2.json", "r") as file:
    data = json.load(file)

entries = [item for item in data if urlparse(item["url"]).netloc == "playtoearn.com"]

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    
    extracted = extract_info(url_content,html_content)
        
    
    results.append(extracted)

print(json.dumps(results, indent=4))
