import streamlit as st
import numpy as np
from urllib.parse import urlencode
import json
from pathlib import Path

from metasearch import search, rank, rank_rrf, preliminary_ranker

st.set_page_config(page_title="MetaSearch")

st.title("MetaSearch")
st.caption("Search across engines. Experiment with ranking.")

query = st.text_input("Search query", placeholder="e.g. learning to rank")
ranker = st.selectbox("Ranking method", ["Preliminary ranker", "RRF", "RankSVM"])

if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("Enter a search query.")
    else:
        engines = ["google", "duckduckgo"]

        with st.spinner("Searching the web..."):
            try:
                clean_query = query.strip()
                results = {engine: search(engine, clean_query) for engine in engines}

                if ranker == "Preliminary ranker":
                    ranked = preliminary_ranker(results, engines)
                    path = Path("dataset.json")

                    data = json.loads(path.read_text()) if path.exists() else {}
                    data[clean_query] = [
                        {
                            "url": url,
                            "title": item["doc"]["title"],
                            "snippet": item["doc"]["snippet"],
                            "link": item["doc"]["link"],
                            "ranks": item["ranks"],
                        }
                        for url, item, score in ranked
                    ]

                    path.write_text(json.dumps(data, indent=2))

                elif ranker == "RRF":
                    ranked = rank_rrf(results, engines)

                else:
                    weights_path = Path("feature_weights.csv")

                    if not weights_path.exists():
                        st.error("feature_weights.csv not found. Train RankSVM first.")
                        ranked = []
                    else:
                        import csv

                        with open(weights_path, "r", newline="") as f:
                            reader = csv.DictReader(f)
                            w = np.array([float(row["weight"]) for row in reader])

                        ranked = rank(clean_query, results, engines, w)

                st.session_state["ranked"] = ranked
                st.session_state["query"] = clean_query
                st.session_state["ranker"] = ranker

            except Exception as e:
                st.error(f"Search failed: {e}")

ranked = st.session_state.get("ranked", [])

if ranked:
    st.divider()
    st.caption(f"RESULTS · {len(ranked)} pages")

    for i, (url, item, score) in enumerate(ranked, 1):
        doc = item["doc"]

        params = urlencode({"q": st.session_state["query"],"url": doc["link"], "pos": i})

        click_url = f"http://127.0.0.1:5001/click?{params}"

        st.markdown(f"### [{doc['title']}]({click_url})")
        st.caption(url)
        st.write(doc["snippet"])
        st.caption(f"Score: {score:.4f}")
        st.divider()
