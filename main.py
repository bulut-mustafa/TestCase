from medium_parser import extract_info as medium_extract_info #most used
from decrypt_parser import extract_info as decrypt_extract_info #second used
from playtoearn_parser import extract_info as playtoearn_extract_info #third used
from qorpoworld_parser import extract_info as qorpoworld_extract_info #fourth used
from blockchaingamer_parser import extract_info as blockchaingamer_extract_info #fifth used
from blog_apeironnft_parser import extract_info as blog_apeironnft_extract_info #sixth used
from dappradar_parser import extract_info as dappradar_extract_info #seventh used
from support_gala_parser import extract_info as support_gala_extract_info #eighth used
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


operations = {
    'medium.com': medium_extract_info,
    'decrypt.co': decrypt_extract_info,
    'chainplay.gg' : decrypt_extract_info,
    'blog.roninchain.com': blog_apeironnft_extract_info,
    'playtoearn.com': playtoearn_extract_info,
    'blog.qorpo.world': qorpoworld_extract_info,
    'www.blockchaingamer.biz': blockchaingamer_extract_info,
    'nftplazas.com': blockchaingamer_extract_info,
    'venturebeat.com' : blockchaingamer_extract_info,
    'blog.apeironnft.com': blog_apeironnft_extract_info,
    'dappradar.com': dappradar_extract_info,
    'support.gala.com': support_gala_extract_info
}


fallback_parsers = [
    medium_extract_info,
    decrypt_extract_info,
    playtoearn_extract_info,
    qorpoworld_extract_info,
    blockchaingamer_extract_info,
    blog_apeironnft_extract_info,
    dappradar_extract_info,
    support_gala_extract_info,
]
with open("dataset2.json", "r") as file:
    data = json.load(file)

entries = [item for item in data ]

results = []

for entry in entries:
    html_content = entry.get("html", "")
    url_content = entry.get("url", "")
    domain = urlparse(entry["url"]).netloc 
    function_to_use = operations.get(domain)
    
    if not function_to_use:
        best_parser = None
        best_result = {
            "url": url_content,
            "author": None,
            "published": None,
            "latestUpdate": None,
        }

        for parser in fallback_parsers:
            try:
                # Attempt to extract data using the current parser
                extracted = parser(url_content, html_content)

                # Count the number of non-None fields in the result
                completeness_score = sum(
                    1 for key in ["author", "published", "latestUpdate"] if extracted.get(key)
                )

                # Update the best parser and result if this one is better
                if completeness_score > sum(
                    1 for key in ["author", "published", "latestUpdate"] if best_result.get(key)
                ):
                    best_parser = parser
                    best_result = extracted
            except Exception as e:
                # Log the error and move to the next parser
                print(f"Error using parser {parser.__name__} for {url_content}: {e}")
                continue

        # Use the best parser or fallback to a default result
            function_to_use = best_parser
            extracted = best_result
    else:
            # Use the originally identified parser
        extracted = function_to_use(url_content, html_content) if function_to_use else {
            "url": url_content,
            "author": None,
            "published": None,
            "latestUpdate": None,
        }
            
            
        
    
    results.append(extracted)

new_dataset = json.dumps(results, indent=4)

# Write the <head> content to a new file
with open("dataset3.json", "w") as output_file:
    output_file.write(new_dataset)