from flask import Flask, jsonify, request
from flask_cors import CORS
import feedparser
import re
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend to connect

def extract_price(title):
    """Extract price from listing title"""
    price_match = re.search(r'\$([0-9,]+)', title)
    if price_match:
        return int(price_match.group(1).replace(',', ''))
    return None

def extract_year(title):
    """Extract year from listing title"""
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', title)
    if year_match:
        return int(year_match.group(1))
    return None

def extract_make_model(title):
    """Extract make and model from title"""
    # Remove price and year
    cleaned = re.sub(r'\$[0-9,]+', '', title)
    cleaned = re.sub(r'\b(19\d{2}|20\d{2})\b', '', cleaned)
    cleaned = cleaned.strip()
    
    # Common makes
    makes = ['toyota', 'honda', 'ford', 'chevrolet', 'chevy', 'nissan', 
             'bmw', 'mercedes', 'audi', 'volkswagen', 'vw', 'mazda', 
             'subaru', 'tesla', 'jeep', 'ram', 'dodge', 'hyundai', 'kia']
    
    make = None
    model = None
    
    words = cleaned.lower().split()
    for i, word in enumerate(words):
        for known_make in makes:
            if known_make in word:
                make = known_make
                # Get next 1-2 words as model
                if i + 1 < len(words):
                    model = ' '.join(words[i+1:i+3])
                break
        if make:
            break
    
    return make or 'unknown', model or cleaned[:30]

def parse_craigslist_feed(feed_url):
    """Parse Craigslist RSS feed and return structured listings"""
    feed = feedparser.parse(feed_url)
    listings = []
    
    for entry in feed.entries:
        price = extract_price(entry.title)
        year = extract_year(entry.title)
        make, model = extract_make_model(entry.title)
        
        # Skip if no price
        if not price:
            continue
        
        # Extract location from description or use default
        location = 'Oregon'
        if hasattr(entry, 'summary'):
            # Try to find location in description
            loc_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s*(OR|WA)', entry.summary)
            if loc_match:
                location = f"{loc_match.group(1)}, {loc_match.group(2)}"
        
        # Parse posted date
        posted_date = datetime.now().isoformat()
        if hasattr(entry, 'published_parsed'):
            posted_date = datetime(*entry.published_parsed[:6]).isoformat()
        
        # Estimate mileage (random for demo - would need to parse from description)
        mileage = None
        mileage_match = re.search(r'(\d+)k?\s*mi', entry.title.lower())
        if mileage_match:
            mileage = int(mileage_match.group(1))
            if mileage < 500:  # Likely in thousands
                mileage *= 1000
        
        # Extract actual Craigslist post URL from entry.link
        post_link = entry.link if hasattr(entry, 'link') else '#'
        
        # Try to get image from media content or enclosures
        image_url = ''
        if hasattr(entry, 'media_content') and entry.media_content:
            image_url = entry.media_content[0].get('url', '')
        elif hasattr(entry, 'enclosures') and entry.enclosures:
            image_url = entry.enclosures[0].get('href', '')
        
        listing = {
            'id': abs(hash(entry.link)),  # Use absolute value for positive ID
            'title': entry.title,
            'make': make,
            'model': model,
            'year': year or 2020,
            'price': price,
            'mileage': mileage or 50000,
            'location': location,
            'source': 'Craigslist',
            'link': post_link,  # Real Craigslist URL
            'posted': posted_date,
            'condition': 'Good',  # Default
            'type': 'sedan',  # Default
            'isDeal': price < 20000,  # Simple logic
            'image': image_url
        }
        
        listings.append(listing)
    
    return listings

@app.route('/api/listings', methods=['GET'])
def get_listings():
    """Get all Oregon and Washington car listings from Craigslist"""
    
    # Get query parameters
    min_price = request.args.get('minPrice', 0, type=int)
    max_price = request.args.get('maxPrice', 1000000, type=int)
    make = request.args.get('make', '').lower()
    max_mileage = request.args.get('maxMileage', 500000, type=int)
    year_from = request.args.get('yearFrom', 1990, type=int)
    
    # All Oregon Craigslist sites
    oregon_sites = [
        'portland',      # Portland
        'eugene',        # Eugene
        'salem',         # Salem
        'corvallis',     # Corvallis
        'bend',          # Bend
        'medford',       # Medford
        'roseburg',      # Roseburg
        'klamath',       # Klamath Falls
        'eastoregon',    # Eastern Oregon
        'oregoncoast',   # Oregon Coast
    ]
    
    # All Washington Craigslist sites
    washington_sites = [
        'seattle',       # Seattle
        'spokane',       # Spokane
        'yakima',        # Yakima
        'kennewick',     # Tri-Cities
        'wenatchee',     # Wenatchee
        'bellingham',    # Bellingham
        'olympic',       # Olympic Peninsula
        'pullman',       # Pullman/Moscow
        'skagit',        # Skagit/Island
    ]
    
    all_sites = oregon_sites + washington_sites
    
    feed_urls = []
    for site in all_sites:
        # Main area
        feed_urls.append(f"https://{site}.craigslist.org/search/cta?format=rss&min_price={min_price}&max_price={max_price}")
    
    all_listings = []
    
    print(f"Fetching from {len(feed_urls)} Craigslist areas in OR/WA...")
    
    for feed_url in feed_urls:
        try:
            listings = parse_craigslist_feed(feed_url)
            all_listings.extend(listings)
            print(f"Fetched {len(listings)} listings from {feed_url}")
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {e}")
            continue
    
    print(f"Total listings before dedup: {len(all_listings)}")
    
    # Remove duplicates based on link (more reliable than title)
    seen_links = set()
    unique_listings = []
    for listing in all_listings:
        if listing['link'] not in seen_links:
            seen_links.add(listing['link'])
            unique_listings.append(listing)
    
    print(f"Total unique listings: {len(unique_listings)}")
    
    # Apply filters
    filtered = unique_listings
    
    if make:
        filtered = [l for l in filtered if make in l['make'].lower()]
    
    filtered = [l for l in filtered if l['mileage'] <= max_mileage]
    filtered = [l for l in filtered if l['year'] >= year_from]
    
    # Sort by posted date (newest first)
    filtered.sort(key=lambda x: x['posted'], reverse=True)
    
    print(f"After filters: {len(filtered)} listings")
    
    return jsonify({
        'success': True,
        'count': len(filtered),
        'listings': filtered[:100]  # Limit to 100 results for performance
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Alpine Seller Search API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        'name': 'Alpine Seller Search API',
        'version': '1.0.0',
        'coverage': 'All Oregon and Washington Craigslist areas',
        'areas': {
            'oregon': ['Portland', 'Eugene', 'Salem', 'Corvallis', 'Bend', 'Medford', 'Roseburg', 'Klamath Falls', 'Eastern OR', 'Oregon Coast'],
            'washington': ['Seattle', 'Spokane', 'Yakima', 'Tri-Cities', 'Wenatchee', 'Bellingham', 'Olympic Peninsula', 'Pullman', 'Skagit']
        },
        'endpoints': {
            '/api/listings': 'Get car listings from all OR/WA Craigslist sites',
            '/api/health': 'Health check'
        },
        'params': {
            'minPrice': 'Minimum price filter',
            'maxPrice': 'Maximum price filter',
            'make': 'Car make filter (toyota, honda, etc)',
            'maxMileage': 'Maximum mileage filter',
            'yearFrom': 'Minimum year filter'
        }
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
