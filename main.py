import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse

def shorten_link(token, url):
    bitlink_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': f'Bearer {token}'}
    body = {'long_url': url}

    response = requests.post(bitlink_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()['id']


def get_clicks(bitlink, token):
    sample_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}

    params = {"units": -1, "unit": "month"}

    response = requests.get(sample_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    check_bitlink = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(check_bitlink, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    url = argparse.ArgumentParser(description="Enter url")
    url.add_argument('url', help='enter url')
    args = url.parse_args()
    url = args.url
    try:
        response = is_bitlink(url,token)
        if response:
            parsed_url = urlparse(url)
            bitlink = f'{parsed_url.netloc}{parsed_url.path}'
            print(f'Total clicks: {get_clicks(bitlink, token)}')
        else:
            print(f'Bitlink: {shorten_link(token, url)}')
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')



if __name__ == '__main__':
    main()

