import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime

def returnUpdatedAt(html_content):
    nbka = html_content.find('updatedAt')
    if(nbka == -1):
        return "No updated date available."
    a = html_content.find(",", nbka + 11)
    b = html_content[nbka + 11:a]
    updated_date = datetime.utcfromtimestamp(int(b) / 1000)
    return updated_date.strftime('%Y-%m-%d %H:%M:%S UTC')

def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a eldarune.medium.com article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    lastUpdate = returnUpdatedAt(html_content)
    
    if '400' in soup.title.string:
        result = {
            "url": url_content,
            "author": "404 Not Found",
            "published": "404 Not Found",
            "latestUpdate": "404 Not Found"
        }
    else:
        site_name = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
        author = soup.find(name='meta', attrs={'name': 'author'})
        published = soup.find(name='meta', attrs={'property': 'article:published_time'})
        
        author_content = author.get('content') if author else "Author not found"
        published_content = published.get('content') if published else "Published date not found"
        
        result = {
            "url": url_content,
            "author": author_content,
            "published": published_content,
            "latestUpdate": lastUpdate,
            'siteName': site_name
        }
    
    return result
with open("dataset2.json", "r") as file:
    data = json.load(file)

entries = [item for item in data if urlparse(item["url"]).netloc == "eldarune.medium.com"]

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    
    
    extracted = extract_info(url_content,html_content)
        
    
    results.append(extracted)

print(json.dumps(results, indent=4))
