import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import re
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a PlayToEarn.com article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    site_name  = soup.find(name='meta', attrs={'property': 'og:site_name'}).get('content')
    author_tag = soup.find('div', class_='__CreatorName')
    author = author_tag.getText() if author_tag else "Author not found"
        
    disclaimer_divs = soup.find_all("div", class_="NewsContentDisclaimer")
    posted_date = "Not found"
    updated_date = "Not found"

    for div in disclaimer_divs:
        if "Posted:" in div.text and "Updated:" in div.text:
            text = div.text
            posted_match = re.search(r"Posted: ([\d]{2} [A-Za-z]{3}, [\d]{4} [\d]{2}:[\d]{2})", text)
            updated_match = re.search(r"Updated: ([\d]{2} [A-Za-z]{3}, [\d]{4} [\d]{2}:[\d]{2})", text)
            posted_date = posted_match.group(1) if posted_match else "Not found"
            updated_date = updated_match.group(1) if updated_match else "Not found"
            break
            
            
    result = {
        "url": url,
        "author": author,
        "published": posted_date,
        "latestUpdate": updated_date,
        'siteName': site_name
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
