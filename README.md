# Alpine Seller Search - Backend API

Real-time car listing aggregator for Oregon and Washington Craigslist.

## Deployed on Railway

This backend scrapes 19 Craigslist sites across Oregon and Washington and provides a REST API.

## Quick Deploy to Railway

1. Fork this repo
2. Go to [railway.app](https://railway.app)
3. Connect this GitHub repo
4. Railway auto-deploys!
5. Generate domain and copy your URL

## API Endpoints

- `GET /` - API info
- `GET /api/listings` - Get all car listings
- `GET /api/health` - Health check

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Tech Stack

- Python 3.11
- Flask
- feedparser (Craigslist RSS)
- CORS enabled
- Gunicorn for production

## Coverage

**Oregon:** Portland, Eugene, Salem, Corvallis, Bend, Medford, Roseburg, Klamath Falls, Eastern Oregon, Oregon Coast

**Washington:** Seattle, Spokane, Yakima, Tri-Cities, Wenatchee, Bellingham, Olympic Peninsula, Pullman, Skagit

## License

MIT
