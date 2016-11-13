#! /usr/bin/python3

import sys
import os
import json

import requests


def download_all(board, thread_num, folder=os.getcwd()):
    r"""Downloads all images in a thread and saves them in a folder.

    Parameters
    ----------
    board : The 4chan board id string.  For example, 'b', 'r9k', etc.
    thread_num : The thread number or post number from the OP. 
    folder : The folder to save the images.  This can be either a absolute or
             a relative path.
             e.g. 'C:\Users\octopuzzy\Pictures' for Windows
                  '/home/octopuzzy/pictures/' for Linux
    """
    # Get image file names
    print('Retrieving thread data ...')
    response = requests.get('https://a.4cdn.org/{}/thread/{}.json'.format(
        board, thread_num))
    response.raise_for_status()
    thread_data = json.loads(response.text)

    # Make the directory
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download the images and save to disk
    for post in thread_data['posts']:
        if 'tim' in post.keys():
            image_name = str(post['tim']) + post['ext']
            print('Downloading image {} ...'.format(image_name))
            response = requests.get('https://i.4cdn.org/{}/{}'.format(
                board, image_name))
            response.raise_for_status()

            # Save to disk
            image_file = open(
                os.path.join(folder, image_name), 'wb')
            for chunk in response.iter_content(1000000):
                image_file.write(chunk)
            image_file.close()
    print('Done')


if __name__ == '__main__':
    board = sys.argv[1]
    thread = int(sys.argv[2])
    folder = os.getcwd()
    download_all(board, thread, folder)
