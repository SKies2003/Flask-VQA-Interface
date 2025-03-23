import requests
from bs4 import BeautifulSoup
import re
import random
import urllib.parse

def get_wikipedia_info(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        extract = response.json().get("extract", "No information found.")
        # Split into paragraphs for better formatting
        return extract.split('\n\n')
    return ["Wikipedia information not available."]

def get_facts(query):
    try:
        # Handle numeric results by converting them to words
        if query.isnumeric():
            number_words = {
                '1': 'number one',
                '2': 'number two',
                '3': 'number three',
                '4': 'number four',
                '5': 'number five',
                '6': 'number six',
                '7': 'number seven',
                '8': 'number eight',
                '9': 'number nine',
                '10': 'number ten'
            }
            query = number_words.get(query, f"number {query}")

        search_url = f"https://www.thefactsite.com/?s={query.replace(' ', '+')}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the first article link
        article_link = soup.find('a', class_='gb-container')['href']
        article_response = requests.get(article_link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Extract facts from the article
        facts = article_soup.select('.entry-content p')
        all_facts = [fact.text.strip() for fact in facts if fact.text.strip()]

        # Return 4-5 facts, trying to skip intro paragraphs
        if len(all_facts) > 4:
            selected_facts = all_facts[2:6]
        elif len(all_facts) > 2:
            selected_facts = all_facts[2:]
        else:
            selected_facts = ["Insufficient facts available."]

        # Add source URL to the facts
        return {
            'facts': selected_facts,
            'source_url': article_link
        }
    except Exception as e:
        return {
            'facts': [f"Error fetching facts: {e}"],
            'source_url': None
        }

def get_youtube_videos(query):
    try:
        # Define different types of video search terms
        video_prefixes = [
            "educational video about",
            "documentary about",
            "explained video about",
            "top facts about",
            "interesting information about"
        ]

        # Randomly select a prefix
        search_prefix = random.choice(video_prefixes)
        search_query = f"{search_prefix} {query}"
        
        # URL encode the search query
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            return []

        # More robust video extraction with title
        video_pattern = re.compile(r'\/watch\?v=([^"&]+).*?"title":{"runs":\[{"text":"([^"]+)"}')
        video_matches = video_pattern.findall(response.text)
        
        # Remove duplicates while preserving order
        unique_videos = list(dict.fromkeys(video_matches))

        # Curate videos
        videos = []
        for video_id, title in unique_videos[:10]:  # Wider search to ensure good results
            try:
                # Construct video details
                videos.append({
                    'video_id': video_id, 
                    'title': title
                })
                
                if len(videos) == 5:
                    break
            except Exception:
                continue

        return videos
    except Exception as e:
        print(f"YouTube video retrieval error: {e}")
        return []