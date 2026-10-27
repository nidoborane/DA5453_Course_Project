import os
import json
import hashlib
import serpapi
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import numpy as np
from features import *

os.environ["SERPAPI_KEY"] = "6d3f95f74dcddf36ed0e08394a5faca1bc078d8cdabca41608faf677ae2261f4"
client = serpapi.Client(api_key=os.environ["SERPAPI_KEY"])

def search(engine, q, k=7):
    return client.search({"engine": engine, "q": q}).get("organic_results", [])[:k]
    
def union(results):
    V = {}

    for engine, docs in results.items():
        for i, r in enumerate(docs, 1):
            url = canonicalize(r["link"])
            doc = {
                "title": r.get("title", ""),
                "link": r["link"],
                "snippet": r.get("snippet", "")
            }
            if url not in V:
                V[url] = {"doc": doc, "ranks": {}}

            V[url]["ranks"][engine] = r.get("position", i)

    return V    

def preliminary_ranker(results, engines):
    V = union(results)
    ranked = []
    seen = set()
    max_len = max((len(results[e]) for e in engines), default=0)

    for i in range(max_len):
        for engine in engines:
            if i >= len(results[engine]):
                continue

            url = canonicalize(results[engine][i]["link"])
            if url not in seen:
                seen.add(url)
                ranked.append((url, V[url], 1 / (len(ranked) + 1)))

    return ranked

def rank_rrf(results, engines):
    V = union(results)
    scores = []
    k0 = 60

    for url, doc in V.items():
        score = 0
        for engine in engines:
            score += 1 / (k0 + V[url]["ranks"][engine])
        scores.append((url, doc, score))
    
    return sorted(scores, key=lambda x: x[2], reverse=True)

def rank(query, results, engines, w):
    V = union(results)
    scores = []

    for url, doc in V.items():
        x = compute_feature_vector(query, url, doc["doc"]["title"], results, engines)
        score = np.dot(w, x)
        scores.append((url, doc, score))

    return sorted(scores, key=lambda x: x[2], reverse=True)
