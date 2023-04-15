import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Ignore SSL certificate errors
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

REGEX_PATTERN = r'(?:"|\')(((?:[a-zA-Z]{1,10}://|//)[^"\'/]{1,}\.[a-zA-Z]{2,}[^"\']{0,})|((?:/|\.\./|\./)[^"\'><,;| *()(%%$^/\\\[\]][^"\'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^"|\']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^"|\']{0,}|)))(?:"|\')'

def extract_links(url):
    """
    Extracts all the links from a given URL using the provided regular expression.
    """
    response = requests.get(url, verify=False)
    html = response.text
    links = re.findall(REGEX_PATTERN, html)
    return [link[0] for link in links]

if __name__ == '__main__':
    url = input('Enter the URL or JS file URL: ')
    links = extract_links(url)
    for link in links:
        print(link)
