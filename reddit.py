#!/usr/bin/python3

import requests as r
from urllib.request import urlretrieve
import os
import time
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
import requests
import shutil

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--subreddit', help='name of the subreddit')
parser.add_argument('--user', help='user name')
parser.add_argument('--sort', default='top', help='top or hot')

args = parser.parse_args()
print(args) 

if args.subreddit:
    sub_reddit = args.subreddit

    if args.sort == 'top':
        url = 'https://www.reddit.com/r/{0}/top.json?sort=top&t=all'.format(sub_reddit)
    else:
        url = 'https://www.reddit.com/r/{0}/.json?'.format(sub_reddit)
elif args.user:
    sub_reddit = args.user
    url = 'https://www.reddit.com/user/{0}.json'.format(sub_reddit)
else:
    raise parser.error('No user or subreddit name')

gfycat = 'https://gfycat.com/cajax/get/{0}'
redgifs = 'https://api.redgifs.com/v1/gfycats/{}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

exceptions = {}
filenames = []

def get_gfycat_url(gfycat_name):
        response = r.get(gfycat.format(gfycat_name), headers=headers)

        if response.status_code == 200:
                response_json = response.json()
                mp4url = response_json['gfyItem']['mp4Url']
                return mp4url
        else:
                return False

def get_redgifs_url(redgifs_name):
        response = r.get(redgifs.format(redgifs_name), headers=headers)

        if response.status_code == 200:
                response_json = response.json()
                mp4url = response_json['gfyItem']['mp4Url']
                return mp4url
        else:
                return False

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def download_media(img_url, file_name, source, folder_name):
    try:
        file_path = folder_name
        if not os.path.exists(file_path):
            print('???', file_path, '????????')
            os.makedirs(file_path)
        
        if source == 'gfycat.com':
                gfycat_name = img_url.split('/')[-1]
                img_url = get_gfycat_url(gfycat_name)
                if img_url:
                        file_suffix = os.path.splitext(img_url)[1]
                        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                        if os.path.exists(filename) or filename in filenames:
                                print("File {0} already exists".format(filename))
                                return False
                        print('\nDownloading gfycat', img_url)
                        filenames.append(filename)
                        urlretrieve(img_url, filename, reporthook)
        elif source == 'i.imgur.com':
                img_url = img_url.replace('.gifv', '.mp4')
                file_suffix = os.path.splitext(img_url)[1]
                filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                if os.path.exists(filename) or filename in filenames:
                                print("File {0} already exists".format(filename))
                                return False
                print('\nDownloading imgur', img_url)
                filenames.append(filename)
                urlretrieve(img_url, filename, reporthook)
        elif source == 'i.redd.it':
                file_suffix = os.path.splitext(img_url)[1]
                filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                if os.path.exists(filename) or filename in filenames:
                                print("File {0} already exists".format(filename))
                                return False
                print('\nDownloading reddit', img_url)
                filenames.append(filename)
                urlretrieve(img_url, filename, reporthook)
        elif source == 'redgifs.com':
                redgifs_name = img_url.split('/')[-1]
                img_url = get_redgifs_url(redgifs_name)
                if img_url:
                        file_suffix = os.path.splitext(img_url)[1]
                        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                        if os.path.exists(filename) or filename in filenames:
                                print("File {0} already exists".format(filename))
                                return False
                        print('\nDownloading redgifs', img_url)
                        filenames.append(filename)
                        with requests.get(img_url, stream=True) as r:
                            with open(filename, 'wb') as f:
                                shutil.copyfileobj(r.raw, f)

        else:
                exceptions[source] = img_url

    except IOError as e:
        print('??????', e)
    except Exception as e:
        print('?? ?', e)


def process_post(post):
    # Identify post download url and source.
    try:
            source = post['data']['domain']
    except KeyError:
            print('No domain in data object')
            return
    media_url = post['data']['url']
    filename = post['data']['title']
    download_media(media_url, filename.replace('/', '_'), source, 'downloads/'+sub_reddit)


def request_reddit(url):
        response = r.get(url, headers=headers)
        if response.status_code == 200:
                response_json = response.json()
                next_page = response_json['data']['after']
                posts = response_json['data']['children']

                with ThreadPoolExecutor(max_workers=16) as runner:
                    for post in posts:
                        runner.submit(process_post, post)

                if next_page is not None:
                        print("\nHeading over to next page ... ")
                        if '?' in url:
                                url = url+'&after='+next_page
                        else:
                                url = url + '?after='+next_page
                        request_reddit(url)
        else:
                print(response)


request_reddit(url)
print(exceptions)
