#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request
import pathlib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  match_host = re.search(r'_([a-zA-Z0-9\.-]+)$', filename)
  
  if match_host:
    hostname = match_host.group(1)
  else:
    sys.exit('Incorrect filename')
    
  url_pattern = re.compile(r'GET (\S+puzzle\S+) HTTP')
  url_list = None
  
  with open(filename) as f:
    url_list = list(set(url_pattern.findall(f.read())))
    
  url_list.sort(key=url_key) 
  result = []
  
  for url in url_list:
    result.append('http://' + hostname + url)  
    
  return result 
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
  i = 0
  img_tags = ''
 
  print('***Attempting to download ' + str(len(img_urls)) + ' images***')
  
  for url in img_urls:
    file_path = os.path.abspath(os.path.join(dest_dir, f'img{str(i)}.jpg'))
    print('--Downloading ' + file_path)
    
    if not os.path.exists(file_path):    
      with open(file_path, 'wb') as f:
        f.write(read_img(url))
    
    img_tags += f'<img src="img{str(i)}.jpg">'
    i += 1
    
  html_path = os.path.abspath(os.path.join(dest_dir, 'index.html'))
  with open(html_path, 'w') as f:
    f.write('<html>\n<body>\n')
    f.write(f'{img_tags}\n')
    f.write('</body>\n</html>')
    
def read_img(url):
  with urllib.request.urlopen(url) as response:
    return response.read()
    
def url_key(url):
  pat = re.compile(r'-\w+-(\w+)\.\w+$')
  match = pat.search(url)
  
  if match:
    return match.group(1)
  else:
    return url

def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
