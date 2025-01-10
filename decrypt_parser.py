import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a Decrypt.co article.
    """
    
    soup = BeautifulSoup(html_content, "html.parser")
    site_name_tag = soup.find(name='meta', attrs={'property': 'og:site_name'})
    site_name = site_name_tag.get('content') if site_name_tag else None
    info_script = soup.find('script', type='application/ld+json')
    if not info_script:
        return {'url':url, 'author':  None, 'published': None, 'latestUpdate': None, 'site_name': site_name}
    
    json_info = json.loads(info_script.getText())
    
    metadata ={'url': url,
               'published' : json_info['datePublished'] if 'datePublished' in json_info else None, 
               'updated' : json_info['dateModified']    if 'dateModified' in json_info else None, 
               'author' : json_info['author']['name'] if 'author' in json_info else None,
               'site': site_name}
    
    
    return metadata
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "decrypt.co"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
       
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))