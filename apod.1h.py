#!/usr/bin/env python3

# Copyright 2025 Roland Amacher

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# <xbar.title>NASA's Astronomy Picture of the Day</xbar.title>
# <xbar.version>v0.9</xbar.version>
# <xbar.author>ra-1974</xbar.author>
# <xbar.author.github>https://github.com/ra-1974/apodswiftbar</xbar.author.github> 
# <xbar.desc>Displays the Astronomy Picture of the Day from NASA</xbar.desc>
# <xbar.image>---</xbar.image>
# <xbar.dependencies>python,beautifulsoup</xbar.dependencies>
# <xbar.abouturl>https://github.com/ra-1974/apodswiftbar</xbar.abouturl>

# <swiftbar.environment>[savepath=default ~/Pictures/Backgrounds/]</swiftbar.environment>

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import urllib.request
from urllib.error import HTTPError, URLError
import subprocess
import tempfile
import base64
import os
from pathlib import Path
import random
from datetime import datetime, timedelta

# some settings
startingpoint = 'https://apod.nasa.gov/apod/'
start_date = datetime(2016, 1, 1)
end_date = datetime.today()

# getting the matching URLs from the page has to go into a function
def create_list(url):
    # Step 1: Fetch the webpage
    response = requests.get(url)

    # Step 2: Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Checking <a> links pointing directly to images
    result = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # not only searching for jpg or png extensions but ensure it is not a full url
        if re.search(r'\.(jpg|png)$', href, re.IGNORECASE) and not re.search(r'https?://', href, re.IGNORECASE):
            result.append(href)

    # Make URLs absolute
    result = [urljoin(url, img_url) for img_url in result]
    return result

def random_date():
    # Calculate the number of days between start and end
    delta_days = (end_date - start_date).days

    # Pick a random number of days to add
    random_days = random.randint(0, delta_days)

    # Compute the random date
    random_date = start_date + timedelta(days=random_days)

    # we need a URL like this: https://apod.nasa.gov/apod/ap250622.html
    return startingpoint + "ap" + random_date.strftime("%y%m%d") + ".html"
    
print('🔭') 
print('---')

# The try block
try:
    image_urls = create_list(startingpoint)
            
    # TODO: if there is not picture of the day available then choose a random one (but for this it would be nice to have the website parsing in a function)
    if not image_urls:
        image_urls = create_list(random_date())
        print("the urls found: ", image_urls)

        # TODO: this should be better, but we have to check a 2nd time if we got something, otherwise giving up
        if not image_urls:
            raise ValueError("no path to a picture (jpg or png) found, probably a video today")

    # Step 4: Output
    # TODO: limiting the output to one URL because it is the "Astronomy Picture of the Day"
    #       -> the current solution isn't nice, just taking the fist element
    image_url = image_urls[0]
    filename = os.path.basename(image_url)

    # Settings
    max_size = 700
    save_dir = Path.home() / "Pictures/Backgrounds"
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / filename

    # 1️⃣ Download image (only if it doesn't already exist)
    if not save_path.exists():
        urllib.request.urlretrieve(image_url, save_path)

    # 2️⃣ Resize using macOS `sips` into a temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_thumb:
        subprocess.run(["sips", "-Z", str(max_size), str(save_path), "--out", tmp_thumb.name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        thumb_path = tmp_thumb.name

    # 3️⃣ Encode thumbnail as Base64
    with open(thumb_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    # 4️⃣ Remove temp thumbnail (keep original in save_dir)
    os.remove(thumb_path)

    # Finally showing the menu item with the thumbnail
    print(f"| href=https://apod.nasa.gov/apod/ image={img_b64}")

except HTTPError as e:
    # e.code has the HTTP status (e.g., 404)
    print(f"HTTP error occurred: {e.code} {e.reason}")
except URLError as e:
    # URL-related errors (e.g., no internet)
    print(f"URL error occurred: {e.reason}")
except Exception as e:
    print("An exception occurred: ", e)
