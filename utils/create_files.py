import json
import os


def save_data_to_file(
    amazon_bucket: str, counries_data: list, output: str = "results"
) -> None:
    """Create manifest for the bucket S3 and countries data as a json files"""

    check_if_output_exist(output)
    with open(f"{output}/CountriesBigMacData.json", "w") as file:
        json.dump(counries_data, file)

    create_json_manifest_s3_bucket(output, amazon_bucket)


def create_json_manifest_s3_bucket(output: str, amazon_bucket: str) -> None:
    """Create config file for S3 bucket"""

    manifest = {
        "fileLocations": [{"URIPrefixes": [f"s3://{amazon_bucket}/"]}],
        "globalUploadSettings": {"format": "JSON"},
    }
    with open(f"{output}/manifest-s3-nasdaq-httpx.json", "w") as file:
        json.dump(manifest, file)

    print("Manifest was created.")


def check_if_output_exist(output: str) -> None:
    """Create new directory, if it doesn't exist"""

    is_exist = os.path.exists(output)
    if not is_exist:
        os.makedirs(output)
