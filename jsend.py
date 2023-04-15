import argparse
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Ignore SSL certificate errors
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

REGEX_PATTERN = r'(?:"|\')(((?:[a-zA-Z]{1,10}://|//)[^"\'/]{1,}\.[a-zA-Z]{2,}[^"\']{0,})|((?:/|\.\./|\./)[^"\'><,;| *()(%%$^/\\\[\]][^"\'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^"|\']{0,}|)))(?:"|\')'

def extract_links_from_url(url):
    """
    Extracts all the links from a given URL using the provided regular expression.
    """
    response = requests.get(url, verify=False)
    html = response.text
    links = re.findall(REGEX_PATTERN, html)
    return [link[0] for link in links]

def extract_links_from_file(file_path):
    """
    Extracts all the links from a file using the provided regular expression.
    """
    with open(file_path, 'r') as f:
        contents = f.read()
    links = re.findall(REGEX_PATTERN, contents)
    return [link[0] for link in links]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract links from a URL or text file')
    parser.add_argument('-u', '--url', type=str, help='The URL to extract links from')
    parser.add_argument('-f', '--file', type=str, help='The path to a text file to extract links from')
    args = parser.parse_args()

    if args.url:
        links = extract_links_from_url(args.url)
    elif args.file:
        links = extract_links_from_file(args.file)
    else:
        print('Either the --url or --file option must be specified.')
        exit()

    for link in links:
        print(link)
