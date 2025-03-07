import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) or (
            not result.scheme and result.netloc and '.' in result.netloc
        )
    except:
        return False

def search_web(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Using DuckDuckGo as search engine (more scraping-friendly)
    search_url = f'https://html.duckduckgo.com/html/?q={query}'
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        web_results = []
        website_results = []
        
        # Parse search results
        results = soup.find_all('div', class_='result')
        
        for result in results[:15]:  # Limit to 15 results
            title_elem = result.find('a', class_='result__a')
            if not title_elem:
                continue
                
            title = title_elem.get_text()
            link = title_elem['href']
            snippet = result.find('a', class_='result__snippet')
            description = snippet.get_text() if snippet else ''
            
            result_data = {
                'title': title,
                'link': link,
                'description': description
            }
            
            # Separate into web and website results
            if any(term in title.lower() for term in ['blog', 'article', 'news', 'post']):
                web_results.append(result_data)
            else:
                website_results.append(result_data)
        
        return web_results, website_results
        
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch search results: {str(e)}")
