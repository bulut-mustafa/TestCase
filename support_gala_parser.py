import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a support.gala.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    author_tag = soup.find(name='meta', attrs={'name': 'author'})
    author_name = author_tag.get('content') if author_tag else None
    site_name_tag = soup.find(name='meta', attrs={'property': 'og:site_name'})
    site_name = site_name_tag.get('content') if site_name_tag else None
    
    meta_group = soup.select_one('ul.meta-group')

    
    if meta_group:
        published = meta_group.find('time', {'datetime': True})
        updated = meta_group.find_all('time', {'datetime': True})[1] if len(meta_group.find_all('time', {'datetime': True})) > 1 else None
    else:
        published = None
        updated = None

    metadata = {
            'url': url,
            'published': published['datetime'],
            'updated': updated['datetime'],
            'author': author_name,
            'site': site_name
        } 
    
    
    return metadata
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "support.gala.com"] 

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
       
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))