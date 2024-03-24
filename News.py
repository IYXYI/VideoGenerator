import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Set up your API key
api_key = 'ac4e95fbca3c4ca6bdabbfb39d047c14'  # Replace 'YOUR_API_KEY' with your actual News API key

# Define the base URL for the News API
base_url = 'https://newsapi.org/v2/everything'

# Define the search query
search_query = 'news'

# Define the parameters for the API request
params = {
    'apiKey': api_key,
    'q': search_query,  # Search query
    'pageSize': 10,  # Number of articles per page
    'language': 'en',  # Language of the articles
    'sortBy': 'publishedAt',  # Sort by publication date
    'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'),  # From 7 days ago
    'to': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # To now
}

# Make the API request
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Extract news articles from the response
    articles = response.json().get('articles', [])
    
    # Check if there are articles
    if articles:
        # Display the headlines, publication time, and URLs of the articles
        for article in articles:
            title = article['title']
            url = article['url']
            published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            
            print(f"Title: {title}")
            print(f"Published At: {published_at}")
            print(f"URL: {url}")
            print()
            
            # Make a request to the article URL
            article_response = requests.get(url)
            
            # Check if the request was successful
            if article_response.status_code == 200:
                # Parse the HTML content of the article
                soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Extract the article content
                content = soup.get_text()
                print(content)
                
                # Add the content to the article object
                article['content'] = content
                
            else:
                print(f"Failed to fetch article content for {title}")
            
            print('-' * 50)  # Separator between articles
            
        # Save articles to a JSON file with content added
        with open('news_articles_with_content.json', 'w') as json_file:
            json.dump(articles, json_file, indent=4)
            
        print("Articles saved to 'news_articles_with_content.json'")
    else:
        print("No articles found.")
else:
    print('Failed to fetch news articles:', response.text)
