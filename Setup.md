# MetaSearch — Setup Instructions

## 1. Install dependencies

Run:

```bash
python -m pip install streamlit flask numpy serpapi
```

## 2. Get your SerpApi API key

1. Create an account at [SerpApi](https://serpapi.com/).
2. Get your API key from your dashboard.
3. Open `metasearch.py` and find:

```python
api_key = "YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual SerpApi key.

## 3. Run the application

Open two terminals in the project directory.

**Terminal 1 — Start the click logging server:**

```bash
python click_server.py
```

**Terminal 2 — Start the Streamlit app:**

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal to use MetaSearch.

## 4. Inspect click data

Clicking a result title logs the search query, destination URL, displayed position, and timestamp to `clicks.db`.

Run the inspection script to view the recorded click data:

```bash
python inspect_clicklog.py
```

## Project files

- `app.py` — Streamlit search interface.
- `metasearch.py` — Search retrieval, result merging, and ranking.
- `features.py` — URL canonicalization and feature extraction.
- `click_server.py` — Flask endpoint for click logging and redirects.
- `click_logger.py` — Stores click events in SQLite.
- `inspect_clicklog.py` — Displays the click database.

## Current status

- Google and Bing search through SerpApi.
- Preliminary feature-based ranking implemented.
- Click logging and SQLite storage implemented.
- RRF and RankSVM options are placeholders and remain to be implemented.
- The click simulator is yet to be implemented.

**Note:** Keep your API key private and never commit it to a public repository.
