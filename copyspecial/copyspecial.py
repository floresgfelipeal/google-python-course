#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def is_special(filename):
  return True if re.search(r'__\w+__', filename) else False
  
def sp_files_list(dir):
  filenames = os.listdir(dir)
  result = []
  
  for filename in filenames:  
    if is_special(filename):
      result.append(os.path.abspath(os.path.join(dir, filename)))
  
  return result
  
def to_dir(orig, dst):
  # copy all the special files located in the directories in "orig" 
  #to the "dst" directory
  if not os.path.exists(dst): os.makedirs(dst)
  
  for dir in orig:
    filenames = os.listdir(dir)
    
    for filename in filenames:  
      if is_special(filename): 
        shutil.copy(os.path.abspath(os.path.join(dir, filename)), dst)
        
def to_zip(zip_file, args):
  files = []
  for arg in args:
    files += sp_files_list(arg)
    
  cmd = '7z a ' + zip_file + ' ' + ' '.join(files)
  print('Command I\'m about to do: ' + cmd)
  
  try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, 
            shell=True)
  except subprocess.CalledProcessError as exc:
    print("Error: ", exc.returncode, exc.output)
  else:
    print(output)
    
def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]
    to_dir(args, todir)

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]
    to_zip(tozip, args)

  if len(args) == 0:
    print("error: must specify one or more dirs")
    sys.exit(1)

  if not todir and not tozip:
    for arg in args:
      print('\n'.join(sp_files_list(arg)))
      
if __name__ == "__main__":
  main()
