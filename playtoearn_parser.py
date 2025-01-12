import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import re
from dateutil.parser import parse
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a PlayToEarn.com article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    site_name  = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
    author_tag = soup.find('div', class_='__CreatorName')
    author = author_tag.getText() if author_tag else None
        
    disclaimer_divs = soup.find_all("div", class_="NewsContentDisclaimer")
    posted_date = None
    updated_date = None

    for div in disclaimer_divs:
        if "Posted:" in div.text and "Updated:" in div.text:
            text = div.text
            posted_match = re.search(r"Posted: ([\d]{2} [A-Za-z]{3}, [\d]{4} [\d]{2}:[\d]{2})", text)
            updated_match = re.search(r"Updated: ([\d]{2} [A-Za-z]{3}, [\d]{4} [\d]{2}:[\d]{2})", text)
            if posted_match:
                try:
                    posted_date = parse(posted_match.group(1)).isoformat()
                except (ValueError, TypeError):
                    posted_date = None
            if updated_match:
                try:
                    updated_date = parse(updated_match.group(1)).isoformat()
                except (ValueError, TypeError):
                    updated_date = None
            break
            
            
    result = {
        "url": url,
        "author": author,
        "published": posted_date,
        "updated": updated_date,
        'site': site_name
    }
    return result
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "playtoearn.com"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
        
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))
