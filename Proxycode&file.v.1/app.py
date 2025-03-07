import os
import logging
from flask import Flask, render_template, request, redirect
from scraper import search_web, is_valid_url
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anura')
def anura():
    return render_template('anura.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')

    if not query:
        return redirect('/')

    # Check if the query is a URL
    if is_valid_url(query):
        if not query.startswith(('http://', 'https://')):
            query = 'https://' + query
        try:
            # Fetch the webpage content
            response = requests.get(query)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Update relative URLs to absolute URLs
            base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(query))
            for tag in soup.find_all(['a', 'img', 'link', 'script']):
                for attr in ['href', 'src']:
                    if tag.get(attr):
                        tag[attr] = urljoin(base_url, tag[attr])

            return render_template('proxy.html', 
                                content=str(soup),
                                original_url=query)
        except Exception as e:
            logger.error(f"Proxy error: {str(e)}")
            return render_template('error.html', error=f"Failed to load website: {str(e)}")

    try:
        # Get search results
        web_results, website_results = search_web(query)
        return render_template('results.html', 
                            query=query,
                            web_results=web_results,
                            website_results=website_results)
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)