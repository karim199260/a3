import sys
import urllib
# sys.path.append("mashape")

from mashape.http.http_client import HttpClient
from mashape.http.content_type import ContentType
from mashape.auth.mashape_auth import MashapeAuth
from mashape.auth.basic_auth import BasicAuth
from mashape.auth.query_auth import QueryAuth
from mashape.auth.custom_header_auth import CustomHeaderAuth
from mashape.auth.oauth_auth import OAuthAuth
from mashape.auth.oauth10a_auth import OAuth10aAuth
from mashape.auth.oauth2_auth import OAuth2Auth


class TextProcessing:

    auth_handlers = []
    PUBLIC_DNS = "japerk-text-processing.p.mashape.com"

    def __init__(self, mashape_key):
        self.auth_handlers.append(MashapeAuth(mashape_key))

    def phrases(self, text, language=None, mashape_callback=None):
        parameters = {
                "language": language,
                "text": text}
        

        mashape_client = HttpClient()
        response = mashape_client.do_call(
                "POST",
                "https://" + self.PUBLIC_DNS + "/phrases/",
                parameters,
                self.auth_handlers,
                ContentType.FORM,
                mashape_callback,
                True)
        return response

    def sentiment(self, text, language=None, mashape_callback=None):
        parameters = {
                "text": text,
                "language": language}
        

        mashape_client = HttpClient()
        response = mashape_client.do_call(
                "POST",
                "https://" + self.PUBLIC_DNS + "/sentiment/",
                parameters,
                self.auth_handlers,
                ContentType.FORM,
                mashape_callback,
                True)
        return response

    def stem(self, text, language=None, stemmer=None, mashape_callback=None):
        parameters = {
                "language": language,
                "stemmer": stemmer,
                "text": text}
        

        mashape_client = HttpClient()
        response = mashape_client.do_call(
                "POST",
                "https://" + self.PUBLIC_DNS + "/stem/",
                parameters,
                self.auth_handlers,
                ContentType.FORM,
                mashape_callback,
                True)
        return response

    def tag(self, text, language=None, output=None, mashape_callback=None):
        parameters = {
                "language": language,
                "output": output,
                "text": text}
        

        mashape_client = HttpClient()
        response = mashape_client.do_call(
                "POST",
                "https://" + self.PUBLIC_DNS + "/tag/",
                parameters,
                self.auth_handlers,
                ContentType.FORM,
                mashape_callback,
                True)
        return response


