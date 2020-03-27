from urllib.parse import urlsplit, urljoin

from django.test import TestCase

# Create your tests here.
location = "../static/upload/2020/03/10/goods/timg_fS4aeDZ.jpg"
# s = location.lstrip("/")
# print(s)
bits = urlsplit(location)
# if  bits.scheme:
#     print(123)
# else:
#     print(000)
if (bits.path.startswith('/') and not bits.scheme and not bits.netloc and '/./' not in bits.path and '/../' not in bits.path):
    if location.startswith('//'):
        location = location[2:]
    location = "127.0.0.1" + location
else:
    location = urljoin("127.0.0.1" + "/XXXXX/", location)
print(location)