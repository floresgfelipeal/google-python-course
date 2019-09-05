#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """ 
  f = open(filename, 'r')
  dict = {}
  year = None
  
  for line in f:
    match_year = re.search(r'>Popularity\s+in\s+(\d\d\d\d)<', line)
    match_names_rank = re.search(
                      r'>(\d+)</td><td>([a-zA-Z]+)</td><td>([a-zA-Z]+)<', line)
    
    if match_year:
      year = match_year.group(1)
    elif match_names_rank:
      dict[match_names_rank.group(2)] = match_names_rank.group(1)
      dict[match_names_rank.group(3)] = match_names_rank.group(1)
    
  result_list = [str(year)]
  for k, v in sorted(dict.items(), key=lambda x : x[0]):
    result_list.append(f'{k} {v}')
    
  f.close()
  return result_list


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print('usage: [--summaryfile] file [file ...]')
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  if summary: 
    for arg in args:
      with open('summary.txt', mode='a') as file:
        file.write('\n'.join(extract_names(arg)))
        file.write('\n\n')
  else:
    for arg in args:
      print(extract_names(arg), '\n')
      
if __name__ == '__main__':
  main()
