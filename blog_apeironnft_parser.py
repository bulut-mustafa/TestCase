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
            
            # Handle `author` field that can be a dict or list
            author_data = json_info.get('author')
            if isinstance(author_data, list):  # If it's a list, use the first element
                author_name = author_data[0].get('name') if author_data else None
            elif isinstance(author_data, dict):  # If it's a dict, get the `name` directly
                author_name = author_data.get('name')
            else:  # Fallback in case `author` is not in the expected structure
                author_name = None
            
            # Extract other metadata
            publisher = json_info.get('publisher', {})
            metadata = {
                'url': url,
                'published': json_info.get('datePublished'),
                'updated': json_info.get('dateModified'),
                'author': author_name,
                'site': publisher.get('name') if publisher else None,
            }
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in URL: {url} - {e}")
            metadata = {
                'url': url,
                'published': None,
                'updated': None,
                'author': None,
                'site': None,
            }
    else:
        print(f"No <script> tag found for URL: {url}")
        metadata = {
            'url': url,
            'published': None,
            'updated': None,
            'author': None,
            'site': None,
        }

    return metadata

# with open("dataset2.json", "r") as file:
#     data = json.load(file)

# entries = [item for item in data if urlparse(item["url"]).netloc == "blog.apeironnft.com"]

# results = []

# for entry in entries:
#     html_content = entry.get("html", "")
#     url_content = entry.get("url", "")
    
#     extracted = extract_info(url_content, html_content)
#     results.append(extracted)

# print(json.dumps(results, indent=4))
