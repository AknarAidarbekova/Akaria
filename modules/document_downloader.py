import os
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError



NTRS_BASE_URL = "https://ntrs.nasa.gov"


def get_document_downloads(document_id):
    url = (
        f"{NTRS_BASE_URL}/api/citations/"
        f"{document_id}/downloads"
    )

    try:
        with urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not isinstance(data, list):
            return {"error": "Unexpected response format from NTRS"}

        return data

    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        return {"error": str(error)}

def download_from_url(relative_url, save_path):
    document_url = f"{NTRS_BASE_URL}{relative_url}"

    try:
        with urlopen(document_url, timeout=60) as response:
            content = response.read()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as document:
            document.write(content)

        return {
            "success": True,
            "path": save_path,
            "size": len(content)
        }
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return {
            "success": False,
            "error": str(error)
        }




if __name__ == "__main__":
    test_document_id = 20150023100

    download_items = get_document_downloads(test_document_id)

    if isinstance(download_items, dict):
        print(download_items)

    else:
        for download_item in download_items:
            if download_item.get("mimetype") == "application/pdf":
                pdf_relative_url = download_item["links"]["pdf"]
                pdf_filename = download_item["name"]

                pdf_save_path = os.path.join(
                    "data",
                    "raw",
                    str(test_document_id),
                    pdf_filename
                )

                result = download_from_url(pdf_relative_url, pdf_save_path)
                print(result)