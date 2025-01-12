import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
def returnUpdatedAt(html_content):
    """Extract and parse the `updatedAt` timestamp from the raw HTML."""
    nbka = html_content.find('updatedAt')
    if nbka == -1:
        return None
    a = html_content.find(",", nbka + 11)
    b = html_content[nbka + 11:a]
    try:
        updated_date = datetime.utcfromtimestamp(int(b) / 1000)
        return updated_date
    except (ValueError, TypeError):
        return None

def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a medium.com article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    lastUpdate = returnUpdatedAt(html_content)
    
    if '400' in soup.title.string:
        result = {
            "url": url,
            "author": None,
            "published": None,
            "updated": None,
            "site" : None
        }
    else:
        site_name = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
        author = soup.find(name='meta', attrs={'name': 'author'})
        published = soup.find(name='meta', attrs={'property': 'article:published_time'})
        
        author_content = author.get('content') if author else None
        published_content = published.get('content') if published else None
        
        parsed_published = None
        if published_content:
            try:
                parsed_published = parse(published_content)
            except (ValueError, TypeError):
                pass

        
        formatted_lastUpdate = lastUpdate.isoformat() if lastUpdate else None
        
        result = {
            "url": url,
            "author": author_content,
            "published": parsed_published.isoformat() if parsed_published else None,
            "updated": formatted_lastUpdate,
            'site': site_name
        }
    
    return result
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "medium.com"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
    
#     extracted = extract_info(url_content,html_content)
        
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))
