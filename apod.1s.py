#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import base64
import urllib.request

# with open("/tmp/temp.jpg", "rb") as image_file:
    # encoded_string = str(base64.b64encode(image_file.read()))[2:][:-1]
# print(encoded_string)
print('🔭') # The telescope emoji is here, if your text editor does not render it
print('---')
url = 'https://apod.nasa.gov/apod/'
req = urllib.request.Request(url)
# try:
r = str(urllib.request.urlopen(req).read())
# print(r)
# print(r.find('.jpg'))
image_url = ""
for i in range(r.find('.jpg'), 0, -1):
    if r[i] != '"':
        image_url = r[i] + image_url
    else:
        break
image_url = image_url + "jpg"
image_url = "https://apod.nasa.gov/apod/" + image_url


image_req = urllib.request.Request(image_url)

image_file = urllib.request.urlopen(image_req).read()
encoded_string = base64.b64encode(image_file)

# except:
    # print("There was an error, most likely with SSL certificates. Click me to fix |href=https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org")
    
# print(r)
# image_string = "image=" + encoded_string
print("| href=# image=" +  str(encoded_string)[2:][:-1])
