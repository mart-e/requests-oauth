import binascii
import hmac
import random
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urlparse, urlunparse
from hashlib import sha1


escape = lambda url: urllib.parse.quote(to_utf8(url), safe='~')

def to_utf8(x):
    """
    Tries to utf-8 encode x when possible 

    If x is a string returns it encoded, otherwise tries to iter x and 
    encode utf-8 all strings it contains, returning a list.
    """
    if isinstance(x, str) or isinstance(x, int): 
        return x
    try:
        l = iter(x)
    except TypeError:
        return x.decode('utf-8')
    return [to_utf8(i) for i in l]

generate_verifier = lambda length=8: ''.join([str(random.randint(0, 9)) for i in range(length)])


class OAuthObject(object):
    def __init__(self, key, secret):
        self.key, self.secret = key, secret


class Consumer(OAuthObject):
    pass


class Token(OAuthObject):
    pass


class SignatureMethod_HMAC_SHA1(object):
    """
    This is a barebones implementation of a signature method only suitable for use 
    for signing OAuth HTTP requests as a hook to requests library.
    """
    name = 'HMAC-SHA1'

    def check(self, request, consumer, token, signature):
        """Returns whether the given signature is the correct signature for
        the given consumer and token signing the given request."""
        built = self.sign(request, consumer, token)
        return built == signature

    def signing_base(self, request, consumer, token):
        pass

    def sign(self, request, consumer, token):
        """Builds the base signature string."""
        key, raw = self.signing_base(request, consumer, token)
        hashed = hmac.new(key.encode(), raw.encode(), sha1)
        # Calculate the digest base 64.
        return binascii.b2a_base64(hashed.digest())[:-1]
