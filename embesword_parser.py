import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a embersword.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    site_name_tag = soup.find(name='meta', attrs={'property': 'og:title'})
    site_name = site_name_tag.get('content') if site_name_tag else None
    info_script = soup.find('script', type='application/ld+json')
    if info_script:
        try:
            json_info = json.loads(info_script.getText())
            metadata ={'url': url,
               'publish_date' : json_info['datePublished'], 
               'update_date' : json_info['dateModified'], 
               'author' : json_info['author']['name'],
               'site_name': site_name}
            
        except json.JSONDecodeError as e:
            metadata = {
                'url': url,
                'publish_date': None,
                'update_date': None,
                'author': None,
                'site_name': site_name
            }
    else:
        metadata = {
            'url': url,
            'publish_date': None,
            'update_date': None,
            'author': None,
            'site_name': site_name
        }
    
    
    return metadata
with open("dataset2.json", "r") as file:
    data = json.load(file)

entries = [item for item in data if urlparse(item["url"]).netloc == "embersword.com" and "/news" in urlparse(item["url"]).path] 

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    
    extracted = extract_info(url_content,html_content)
       
    
    results.append(extracted)

print(json.dumps(results, indent=4))