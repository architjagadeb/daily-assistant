import urllib.request
from config import NEWS_SOURCES
from main import generate

def fetch_headlines(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        raw = response.read().decode('utf-8')
    
    # Extract top 5 headlines
    headlines = []
    items = raw.split('<item>')
    for item in items[1:6]:
        title_start = item.find('<title>') + 7
        title_end = item.find('</title>')
        title = item[title_start:title_end].strip()
        if title:
            headlines.append(title)
    
    return headlines

def get_news_summary():
    all_headlines = []
    
    for source in NEWS_SOURCES:
        try:
            headlines = fetch_headlines(source["url"])
            for h in headlines:
                all_headlines.append(f"[{source['name']}] {h}")
        except Exception as e:
            print(f"Could not fetch from {source['name']}: {e}")
    
    if not all_headlines:
        return "Could not fetch news today."
    
    prompt = f"""Here are today's top news headlines:
{chr(10).join(f'- {h}' for h in all_headlines)}

Summarize these in 4-5 lines in a friendly morning briefing style."""
    
    return generate(prompt)

if __name__ == "__main__":
    print(get_news_summary())