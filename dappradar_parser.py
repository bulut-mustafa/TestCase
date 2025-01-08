import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_info(url: str, html_content: str) -> dict:
    """
    A snippet to extract author, publish date, and update date from a dappradar.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    info_script = soup.find('script', type='application/ld+json')
    if info_script:
        try:
            json_info = json.loads(info_script.get_text(strip=True))
            
            site_name_tag = soup.find('meta', attrs={'property': 'og:site_name'})
            site_name = site_name_tag.get('content') if site_name_tag else None
            
            
            metadata = {
                'url': url,
                'publish_date': json_info.get('datePublished'),
                'update_date': json_info.get('dateModified'),
                'author': json_info.get('author'),
                'site_name': site_name,
            }
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in URL: {url} - {e}")
            metadata = {
                'url': url,
                'publish_date': None,
                'update_date': None,
                'author': None,
                'site_name': None,
            }
    else:
        print(f"No <script> tag found for URL: {url}")
        metadata = {
            'url': url,
            'publish_date': None,
            'update_date': None,
            'author': None,
            'site_name': None,
        }
    
    return metadata

with open("dataset2.json", "r") as file:
    data = json.load(file)

entries = [item for item in data if urlparse(item["url"]).netloc == "dappradar.com"]

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    
    extracted = extract_info(url_content, html_content)
    results.append(extracted)

print(json.dumps(results, indent=4))
