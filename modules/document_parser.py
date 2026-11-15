import pymupdf
import os
import json

def extract_pdf_text(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_index in range(document.page_count):
        page = document.load_page(page_index)
        images = page.get_images(full=True)
        text = page.get_text()

        pages.append({
            "page": page_index + 1,
            "text": text,
            "image_count": len(images)
        })

    document.close()

    return pages

def extract_page_images(pdf_path, page_number):
    document = pymupdf.open(pdf_path)

    page = document.load_page(page_number - 1)
    images = page.get_images(full=True)

    page_13_images = []

    for image_index, image_info in enumerate(images, start=1):
        xref = image_info[0]
        rectangles = page.get_image_rects(xref)

        image_position = []

        for rectangle in rectangles:
            image_position.append({
                "x0": rectangle.x0,
                "y0": rectangle.y0,
                "x1": rectangle.x1,
                "y1": rectangle.y1,
            })

        image_item = document.extract_image(xref)
        width = image_item["width"]
        height = image_item["height"]

        page_13_images.append({
            "image_number": image_index,
            "extension": image_item["ext"],
            "image_bytes": image_item["image"],
            "position": image_position,
            "width": width,
            "height": height
        })

    document.close()
    return page_13_images

if __name__ == "__main__":
    test_pdf_path = "data/raw/20150023100/20150023100.pdf"

    extracted_images = extract_page_images(test_pdf_path, 13)

    output_dir = "data/processed/page_13"
    os.makedirs(output_dir, exist_ok=True)

    for image_data in extracted_images:
        image_path = os.path.join(
            output_dir,
            f"image_{image_data['image_number']}.{image_data['extension']}"
        )

        with open(image_path, "wb") as image_file:
            image_file.write(image_data["image_bytes"])

        print(f"Saved {image_path}")
        print(f"Positions: {image_data['position']}")
        print(
            f"Resolution: "
            f"{image_data['width']}, {image_data['height']} pixels"
        )

    image_metadata = []

    for image_data in extracted_images:
        image_metadata.append({
            "image_number": image_data["image_number"],
            "extension": image_data["extension"],
            "width": image_data["width"],
            "height": image_data["height"],
            "position": image_data["position"]
        })

    metadata_path = os.path.join(output_dir, "metadata.json")

    with open(metadata_path, "w") as metadata_file:
        json.dump(
            image_metadata,
            metadata_file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Metadata saved: {metadata_path}")

    # for page_data in extracted_pages:
    #     print(
    #         f"Page {page_data['page']}: "
    #         f"{page_data['image_count']} images"
    #     )
    #
    #
    #     if len(page_data["text"].strip()) < 150:
    #         print(f"\n PAGE {page_data['page']}")
    #         print(page_data["text"])
    #
    #
    #     text_length = len(page_data["text"])
    #
    #     print(
    #         f"Page {page_data['page']}"
    #         f"{text_length} characters"
    #     )