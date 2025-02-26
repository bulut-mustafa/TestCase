import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import re
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a blog.qorpo.world article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    site_name_tag = soup.find('p', class_='trademark')
    site_name = site_name_tag.getText().split('©')[0].strip() if site_name_tag else None
    
    
    author_tag = soup.find('p', class_='article-owner')
    author = author_tag.getText().replace("Blog By", "").strip() if author_tag else None
    
    
    publish_tag = soup.find('p', class_='article-time')
    publish_date = None

    if publish_tag:
        publish_text = re.sub(r", \d+\s?mins?", "", publish_tag.get_text(strip=True))
        try:
            publish_date = parse(publish_text).isoformat()
        except (ValueError, TypeError):
            publish_date = None
    
            
    result = {
        "url": url,
        "author": author,
        "published": publish_date,
        "updated": None,
        'site': site_name
    }
    return result
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "blog.qorpo.world"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
        
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))
