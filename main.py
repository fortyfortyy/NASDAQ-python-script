import asyncio
import aiohttp
import environ
import requests

from utils.send_notification_email import send_email
from utils.upload_into_s3 import upload_file_to_s3
from utils.create_files import save_data_to_file


env = environ.Env()
environ.Env.read_env()

NASDAQ_API_KEY = env("NASDAQ_API_KEY")
SEND_FROM = env("SEND_FROM")
SEND_TO = env("SEND_TO")
EMAIL_PASSWORD = env("EMAIL_PASSWORD")

AMAZON_BUCKET = env("AMAZON_BUCKET")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

LIMIT_REQUESTS = asyncio.Semaphore(2)
COUNTRIES_DATA = []


async def get_countries_data():
    async with aiohttp.ClientSession(
        trust_env=True, connector=aiohttp.TCPConnector()
    ) as session:
        tasks = get_urls_tasks(session)

        responses = await asyncio.gather(*tasks)
        return responses


async def make_one_request(url, session):
    async with LIMIT_REQUESTS:
        return await session.get(url)


def get_countries_code() -> dict:
    """Get code from each country from given csv file.
    :return Dictionary that contains country: country code"""

    coutries_code = {}
    codes_csv = requests.get(
        "https://static.quandl.com/ECONOMIST_Descriptions/economist_country_codes.csv"
    )

    # clean data from whitespaces etc.
    for row in codes_csv.text.strip("").split("\r"):
        row = row.strip()
        if not row:
            continue

        country, code = row.split("|")
        if country == "COUNTRY":
            continue

        coutries_code[country] = code

    return coutries_code


def get_urls_tasks(session) -> list:
    """Return urls to get data from"""

    urls = []
    countries_code = get_countries_code()

    for code in countries_code.values():
        url = f"https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{code}?api_key={NASDAQ_API_KEY}"
        urls.append(asyncio.create_task(make_one_request(url, session)))

    return urls


def extract_data_from_response(response: dict) -> None:
    """Extract data from nasdaq json object of the given country
    :param response: The data of the given country, formated as a JSON object
    """

    country = {"name": response["dataset"]["name"]}

    bigMacColums = response["dataset"]["column_names"]
    bigMacDate = response["dataset"]["data"][2]

    for idx in range(len(bigMacColums)):
        country[bigMacColums[idx]] = bigMacDate[idx]
    COUNTRIES_DATA.append(country)


async def main() -> None:
    for response in await get_countries_data():
        extract_data_from_response(response=await response.json())

    save_data_to_file(amazon_bucket=AMAZON_BUCKET, counries_data=COUNTRIES_DATA)
    is_uploaded = upload_file_to_s3(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AMAZON_BUCKET,
        "CountriesBigMacData.json",
    )
    if is_uploaded:
        send_email(EMAIL_PASSWORD, send_from=SEND_FROM, send_to="example@gmail.com")
        print("Data has been saved in S3 and email notification was sent.")
    else:
        print("Data was not correctly uploaded into S3 bucket.")


if __name__ == "__main__":
    asyncio.run(main())
