import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import re
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a nftplazas.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    site_name  = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
    author = soup.find(name='meta', attrs={'name': 'author'}).get('content')
    published_date = soup.find(name='meta', attrs={'property': 'article:published_time'})
    published = parse(published_date.get('content')).isoformat() if published_date else None
    updated_date = soup.find(name='meta', attrs={'property': 'article:modified_time'})
    updated = parse(updated_date.get('content')).isoformat() if updated_date else None

       
    result = {
        "url": url,
        "author": author,
        "published": published,
        "updated": updated,
        'site': site_name
    }
    return result
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "nftplazas.com"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
        
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))
