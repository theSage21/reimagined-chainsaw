#! /usr/bin/python
import requests
import re
import sys
from html import unescape

if (len(sys.argv) > 1) and (sys.argv[1] in ['--help', '-help', '--h', '-h', 'help', '--?', '-?']):
    print("""
    gn-Google News
    --------------

    Usage:
    -----

    - press any key to contune reading the news.
    - press 'q' to quit
    """)
    sys.exit(0)


HEAD='\033[94m'
ENDC='\033[0m'

def getch():
    "For getting a single character from the terminal since input waits for the Return key"
    import termios
    import tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch



print('Getting frontpage...')
page = requests.get('https://news.google.com/')

print('Extracting stories')
stories = re.compile(r'span class="titletext">(.*?)</span>.*?div class="esc-lead-snippet-wrapper">(.*?)</div>').findall(page.text)

print(len(stories), 'stories obtained')
get = getch()
for story in stories:
    title, body = story
    print(HEAD, unescape(title), ENDC)
    body = unescape(body)
    while len(body) > 0:
        print('  ', body[:80])
        body = body[80:]
    temp = get()
    if temp in ['q', 'Q']:
        break
