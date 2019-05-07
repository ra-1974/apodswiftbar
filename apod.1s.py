#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import base64

with open("/tmp/temp.jpg", "rb") as image_file:
    encoded_string = str(base64.b64encode(image_file.read()))[2:][:-1]
# print(encoded_string)
print('🔭')
print('---')
image_string = "image=" + encoded_string
print("| href=# image=" +  encoded_string)
