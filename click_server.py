from flask import Flask, request, redirect, abort
from urllib.parse import urlparse
from click_logger import logger

app = Flask(__name__)

@app.get("/click")
def click():
    query = request.args.get("q", "")
    url = request.args.get("url", "")
    position = request.args.get("pos", type=int)

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        abort(400)

    if not query or position is None or position < 1:
        abort(400)

    logger(query, url, position)
    return redirect(url)

if __name__ == "__main__":
    app.run(port=5001, debug=False)
