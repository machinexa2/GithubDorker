from lib.ColoredObject import Color as Cobj
from os import getenv

ColorObj = Cobj()

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36',
    'X-Bug-Bounty': ''
}

try:
    Headers['X-Bug-Bounty'] = getenv('HACKERONE_ACCESS_TOKEN')
except Exception:
    pass
try:
    github_access_token = getenv('GITHUB_ACCESS_TOKEN')
except Exception as E:
    print(f"{ColorObj.bad} No access token provided. Error {E} occured. Check Globals.py")
    exit()


search_regex = [
        "pwd|pass|password|host|username|usr|db_"
]

hexchar = "1234567890abcdefABCDEF"
base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
