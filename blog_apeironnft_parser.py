import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_info(url: str, html_content: str) -> dict:
    """
    A snippet to extract author, publish date, and update date from a blog.apeironnft.com article.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    info_script = soup.find('script', type='application/ld+json')
    if info_script:
        try:
            json_info = json.loads(info_script.get_text(strip=True))
            
            author = json_info.get('author', [{}])[0]  # Safely get the first author if available
            publisher = json_info.get('publisher', {})
            
            metadata = {
                'url': url,
                'publish_date': json_info.get('datePublished'),
                'update_date': json_info.get('dateModified'),
                'author': author.get('name') if author else None,
                'site_name': publisher.get('name') if publisher else None,
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

entries = [item for item in data if urlparse(item["url"]).netloc == "blog.apeironnft.com"]

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    
    extracted = extract_info(url_content, html_content)
    results.append(extracted)

print(json.dumps(results, indent=4))
