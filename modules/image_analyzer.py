from pathlib import Path
import json
from PIL import Image


def load_image_metadata(metadata_path):
    metadata_path = Path(metadata_path)

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_path}"
        )

    with open(metadata_path, "r", encoding="utf-8") as metadata_file:
        metadata = json.load(metadata_file)

    return metadata

def classify_image_by_size(source_image_data):
    width, height = source_image_data["width"], source_image_data["height"]

    area = width * height
    aspect_ratio = width / height

    if area < 30000:
        return "likely_decorative"

    if area > 200000 and 0.8 <= aspect_ratio <= 2.0:
        return "likely_content"

    return "uncertain"

def create_thumbnail(image_path, output_path, max_size=(400,400)):
    image_path = Path(image_path)
    output_path = Path(output_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as source_image:
        source_image.thumbnail(max_size)
        source_image.save(output_path)

        thumbnail_size = source_image.size


    return {
        "success": True,
        "path": str(output_path),
        "size": thumbnail_size
    }


if __name__ == "__main__":
    test_metadata_path = "data/processed/page_13/metadata.json"

    images = load_image_metadata(test_metadata_path)

    print(f"Total images: {len(images)}")

    for image_data in images:
        print(
            f"Image {image_data['image_number']}"
            f"{image_data['width']},{image_data['height']}"
            f"({image_data['extension']}"
        )

    print("\nImage classification: ")

    for image_data in images:
        classification = classify_image_by_size(image_data)

        print(
            f"Image {image_data['image_number']}"
            f"{classification}"
        )

    thumbnail_result = create_thumbnail(
        "data/processed/page_13/image_2.jpeg",
        "data/processed/thumbnails/image_2.jpeg"
    )

    print("\nThumbnail result:")
    print(thumbnail_result)