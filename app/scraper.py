import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_site(url):
    # try url to see if it exists
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Error] Could not fetch {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ## get the required identifiers now
    
    # title
    title = soup.title.string.strip() if soup.title else ""
    
    # meta description
    description = ""
    desc_tag = soup.find("meta", attrs= {"name" : "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()
        
    # h1/h2 tags
    h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1")]
    h2_tags = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
    
    # outbound links
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    outbound_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("http") and urlparse(href).netloc != domain:
            outbound_links.append(href)
            
    # visible text content
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    text_content = soup.get_text(separator=' ', strip=True)
    
    return {
        "title": title,
        "meta_description": description,
        "h1_tags": h1_tags,
        "h2_tags": h2_tags,
        "outbound_links": outbound_links,
        "content": text_content
    }
    