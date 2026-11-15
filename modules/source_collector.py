import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

NTRS_HEALTH_URL = "https://ntrs.nasa.gov/api/health"

def check_ntrs_connection():
    try:
        with urlopen(NTRS_HEALTH_URL, timeout=20) as response:
            result = response.read().decode("utf-8")

            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass

            return {
                "connected": response.status == 200,
                "status_code": response.status,
                "response": result,
            }
    except (URLError, HTTPError, TimeoutError) as error:
        return{
            "connected": False,
            "error": str(error),
            }

NTRS_SEARCH_URL = "https://ntrs.nasa.gov/api/citations/search"

def search_ntrs(query, limit=10):
    import urllib.parse

    params = urllib.parse.urlencode({
        "q": query,
        "page.size": limit
    })

    url = f"{NTRS_SEARCH_URL}?{params}"

    try:
        with urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError) as error:
        return {error:str(error)}

def extract_basic_metadata(data):
    normalized_records = []

    for item in data.get("results", []):
        record = {
            "id": item.get("id"),
            "title": item.get("title"),
            "abstract": item.get("abstract"),
            "keywords": item.get("keywords", []),
            "categories": item.get("subjectCategories", []),
            "document_type": item.get("stiType"),
            "publication_date": item.get("distributionDate"),
            "modified": item.get("modified"),
            "center": item.get("center", {}).get("name"),
            "downloads": item.get("downloads", []),
        }

        normalized_records.append(record)

    return normalized_records

if __name__ == "__main__":
    results = search_ntrs("microgravity combustion", limit=3)
    records = extract_basic_metadata(results)

    print(json.dumps(records,
                     indent=4,
                     ensure_ascii=False
                     ))