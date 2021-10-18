#!/usr/bin/python3

import argparse
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

import requests as r
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-s', '--sort', default='top', help='top or hot')
parser.add_argument('-r', '--subreddit', help='name of the subreddit')
parser.add_argument('-u', '--user', help='user name')
parser.add_argument('-t', '--threads', type=int, default=1, help='parallel threads per page amount, default 1')
parser.add_argument('-i', '--images-only', action='store_true', help='Download only files with content-type images')

args = parser.parse_args()

if args.subreddit:
    sub_reddit = args.subreddit

    if args.sort == 'top':
        url = 'https://www.reddit.com/r/{0}/top.json?sort=top&t=all'.format(sub_reddit)
    elif args.sort == 'hot':
        url = 'https://www.reddit.com/r/{0}/.json?'.format(sub_reddit)
    else:
        raise parser.error('Unsupported sorting mode')
elif args.user:
    sub_reddit = args.user
    url = 'https://www.reddit.com/user/{0}.json'.format(sub_reddit)
else:
    raise parser.error('No user or subreddit name')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

exceptions = {}
downloads = []


def get_url(domain_name, name):
    urls = {
        'gfycat.com': 'https://gfycat.com/cajax/get/{0}',
        'redgifs.com': 'https://api.redgifs.com/v1/gfycats/{}',
    }
    response = r.get(urls[domain_name].format(name), headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        mp4url = response_json['gfyItem']['mp4Url']
        return mp4url
    else:
        return False


def http_download(img_url, folder_name, file_name, timeout):
    if img_url in downloads:
        return False

    downloads.append(img_url)
    file_suffix = os.path.splitext(img_url)[1]
    filename = '{}{}{}{}'.format(folder_name, os.sep, file_name, file_suffix)

    if os.path.exists(filename):
        start_position = os.stat(filename).st_size
    else:
        start_position = 0

    header = r.head(img_url, timeout=timeout)
    total_size = int(header.headers.get('content-length'))
    content_type = header.headers.get('content-type')

    if content_type and args.images_only and not content_type.startswith('image/'):
        return False

    if start_position >= total_size:
        return

    headers = None
    if start_position > 0:
        headers = {'Range': f'{start_position}-{total_size}'}

    resp = r.get(img_url, stream=True, timeout=timeout, headers=headers)

    with open(filename, 'wb') as f, tqdm(
        desc=img_url, total=total_size, unit='B', unit_scale=True, leave=False) as pbar:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                bytes = f.write(chunk)
                pbar.update(bytes)


def download_media(img_url, file_name, source, folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)

        if source in ['gfycat.com', 'redgifs.com']:
            name = img_url.split('/')[-1]
            img_url = get_url(source, name)
        elif source in ['i.imgur.com', 'i.redd.it']:
            img_url = img_url.replace('.gifv', '.mp4')
        else:
            exceptions[source] = img_url
            return

        if img_url:
            http_download(img_url, folder_name, file_name, 10)
    except IOError as e:
        print('??????', e)
    except Exception as e:
        print('?? ?', e)


def process_post(post):
    try:
        download_media(
            post['data']['url'],
            post['data']['title'].replace('/', '_'),
            post['data']['domain'],
            'downloads/{}'.format(sub_reddit))
    except KeyError:
        pass


def request_reddit(media_url, workers):
    response = r.get(media_url, headers=headers, timeout=10)
    if response.status_code == 200:
        response_json = response.json()
        next_page = response_json['data']['after']
        posts = response_json['data']['children']

        with ThreadPoolExecutor(max_workers=workers) as runner:
            for post in posts:
                runner.submit(process_post, post)

            if next_page is not None:
                if '?' in media_url:
                    media_url = media_url + '&after=' + next_page
                else:
                    media_url = media_url + '?after=' + next_page
                runner.submit(request_reddit, media_url, workers)
    else:
        print(response)


request_reddit(url, args.threads)
print(exceptions)
