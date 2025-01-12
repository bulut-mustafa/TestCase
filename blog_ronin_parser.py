import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil.parser import parse
def extract_info(url: str, html_content: str) -> dict:
    """"
    A snippet to extract author, publish date, and update date from a blog.roninchain.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    author_tag = soup.find(name='meta', attrs={'name': 'author'})
    author_name = author_tag.get('content') if author_tag else None
    site_name_tag = soup.find(name='meta', attrs={'property': 'og:title'})
    site_name = site_name_tag.get('content') if site_name_tag else None
    info_script = soup.find('script', type='application/ld+json')
    if info_script:
        try:
            json_info = json.loads(info_script.getText())
            metadata ={'url': url,
               'published' : parse(json_info['datePublished']).isoformat() if 'datePublished' in json_info else None, 
               'updated' : parse(json_info['dateModified']).isoformat() if 'dateModified' in json_info else None, 
               'author' : author_name,
               'site': site_name}
            
        except json.JSONDecodeError as e:
            metadata = {
                'url': url,
                'published': None,
                'updated': None,
                'author': None,
                'site': site_name
            }
    else:
        metadata = {
            'url': url,
            'published': None,
            'updated': None,
            'author': None,
            'site': site_name
        }
    
    
    return metadata
# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "blog.roninchain.com"] 

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content,html_content)
       
    
#     results.append(extracted)

# print(json.dumps(results, indent=4))