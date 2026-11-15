import requests


PSI_SEARCH_URL = "https://psi.nasa.gov/geode-py/ws/repo/search"


def search_psi_investigations(query, limit=10):
    headers = {
        "Accept": "application-json",
        "user_token": ""
    }

    params = {
        "term": query,
        "source": "psi",
        "type": "investigation",
        "from": 0,
        "size": limit
    }

    try:
        response = requests.get(
            PSI_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        hits = data.get("hits", {})
        results = hits.get("hits", [])

        records = [
            item.get("_source", {})
            for item in results
        ]

        return {
            "success": True,
            "total": hits.get("total", 0),
            "records": records
        }

    except (requests.RequestException, ValueError) as error:
        return {
            "success": False,
            "error": str(error),
            "total": 0,
            "records": []
        }


def normalize_psi_research(record):
    return {
        "id": record.get("Accession"),
        "name": record.get("Title"),
        "program": "NASA",
        "research_type": record.get("Research Area"),

        "gravity": (
            "microgravity"
            if "microgravity" in record.get("Approach", "").lower()
            else None
        ),
        "oxygen_concentration": None,
        "fuel_type": [
            fuel
            for fuel in ["methane", "ethylene"]
            if fuel.lower() in record.get("Approach", "").lower()
        ],
        "airflow": (
            "coflow of air"
            if "coflow" in record.get("Approach", "").lower()
            else None
        ),

        "objectives": [
            record["Objectives"]
        ] if record.get("Objectives") else [],

        "hypothesis": {
            "description": record.get("Hypothesis"),
            "status": "Research hypothesis, not a confirmed finding"
        } if record.get("Hypothesis") else None,

        "experimental_setup": {
            "location": record.get("Flight Platform"),
            "approach": record.get("Approach"),
            "hardware": record.get("Experiment Hardware")
        },

        "findings": [],
        "limitations": [],

        "source_url": (
            f"https://psi.nasa.gov/physci/repo/data/"
            f"investigations/{record.get('Accession')}"
        )
    }