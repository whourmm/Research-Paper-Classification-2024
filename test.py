from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import os, json

def scrape_google_scholar_author():
    params = {
        "api_key": os.getenv("API_KEY"),      # SerpApi API key
        "engine": "google_scholar_author",    # author results search engine
        "author_id": "VxOmZDgAAAAJ",          # search query
        "hl": "en"                            # language
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if not results:
        print("Error: No data received from SerpApi. Check API key or author_id.")
        return

    author_results_data = {
        "author_data": {},
        "author_articles": []
    }

    author = results.get("author", {})
    author_results_data["author_data"]["name"] = author.get("name", "Unknown")
    author_results_data["author_data"]["email"] = author.get("email", "Unknown")
    author_results_data["author_data"]["website"] = author.get("website", "Unknown")
    author_results_data["author_data"]["interests"] = author.get("interests", [])
    author_results_data["author_data"]["affiliations"] = author.get("affiliations", "Unknown")
    author_results_data["author_data"]["thumbnail"] = author.get("thumbnail", "")

    author_results_data["author_data"]["cited_by_table"] = results.get("cited_by", {}).get("table", [])
    author_results_data["author_data"]["cited_by_graph"] = results.get("cited_by", {}).get("graph", [])

    author_results_data["author_data"]["public_access_link"] = results.get("public_access", {}).get("link", "")
    author_results_data["author_data"]["public_access_available"] = results.get("public_access", {}).get("available", 0)
    author_results_data["author_data"]["public_access_not_available"] = results.get("public_access", {}).get("not_available", 0)
    author_results_data["author_data"]["co_authors"] = results.get("co_authors", [])

    # Extract articles
    while True:
        results = search.get_dict()

        for article in results.get("articles", []):
            print(f"Extracting article: {article.get('title', 'Unknown')}")

            author_results_data["author_articles"].append({
                "article_title": article.get("title", "Unknown"),
                "article_link": article.get("link", ""),
                "article_year": article.get("year", "Unknown"),
                "article_citation_id": article.get("citation_id", ""),
                "article_authors": article.get("authors", []),
                "article_publication": article.get("publication", ""),
                "article_cited_by_value": article.get("cited_by", {}).get("value", 0),
                "article_cited_by_link": article.get("cited_by", {}).get("link", ""),
                "article_cited_by_cites_id": article.get("cited_by", {}).get("cites_id", "")
            })

        if "next" in results.get("serpapi_pagination", {}):
            search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
        else:
            break

    print(json.dumps(author_results_data, indent=2, ensure_ascii=False))
    print(f"Done. Extracted {len(author_results_data['author_articles'])} articles.")

    # Save to CSV
    pd.DataFrame(data=author_results_data["author_articles"]).to_csv(
        f"{author_results_data['author_data']['name'].lower().replace(' ', '_')}_author_articles.csv", 
        encoding="utf-8"
    )

    return author_results_data

scrape_google_scholar_author()
