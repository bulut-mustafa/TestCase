import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil.parser import parse
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

    published_date = None
    updated_date = None

    
    if meta_group:
        time_tags = meta_group.find_all('time', {'datetime': True})

        if len(time_tags) > 0:
            published_date = time_tags[0].get('datetime')  
            if len(time_tags) > 1:
                updated_date = time_tags[1].get('datetime')  

    try:
        published_date = parse(published_date).isoformat() if published_date else None
        updated_date = parse(updated_date).isoformat() if updated_date else None
    except ValueError:
        pass

    metadata = {
            'url': url,
             'published': published_date,
            'updated': updated_date,
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