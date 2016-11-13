#! /usr/bin/python3

import sys
import os

import requests
from bs4 import BeautifulSoup


def download_all(board, thread_num, folder=os.getcwd()):
    r"""Downloads all images in a thread and saves them in a folder.

    Parameters
    ----------
    board : The 4chan board id string.  For example, 'b', 'r9k', etc.
    thread_num : The thread number or post number from the OP. 
    folder : The folder to save the images.  This can be either a absolute or
             a relative path.
             e.g. 'C:\Users\hawaiianpizza\Pictures' for Windows
                  '/home/hawaiinpizza/pictures/' for Linux
    """
    # Get the html of the thread
    print('Downloading html of thread...')
    response = requests.get('https://boards.4chan.org/{}/thread/{}'.format(
        board, thread_num))
    response.raise_for_status()

    # Get tags of all posted images
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.findAll('a', {'class': 'fileThumb'})

    # Make the directory
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download the images and save to disk
    for tag in image_tags:    
        image_name = tag.get('href').split('/')[-1]
        print('Downloading image {} ...'.format(image_name))
        response = requests.get('https:{}'.format(tag.get('href')))
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
