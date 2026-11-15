from modules.psi_collector import search_psi_investigations
from modules.psi_collector import normalize_psi_research


result = search_psi_investigations("combustion", limit=5)

print("Success:", result["success"])
print("Total results:", result["total"])
print("Downloaded records:", len(result["records"]))

if result["success"] and result["records"]:
    first = result["records"][0]

    print("\nFirst research:")
    print("Title:", first.get("Title"))
    print("Accession:", first.get("Accession"))
    print("Objectives:", first.get("Objectives"))

if result["success"] and result["records"]:
    normalized = normalize_psi_research(result["records"][0])

    print("\nNormalized Akaria record:")
    print(normalized)