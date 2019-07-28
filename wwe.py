#! /usr/bin/python3

import os
import subprocess
from time import time
import json
import requests

HEADERS = {
    'User-Agent': 'okhttp/3.12.1'
}

REALM_HEADERS = {
    'x-api-key': '640a69fb-68b1-472c-ba4b-36f50288c984',
    'realm': 'dce.wwe'
}

DICE_MOBILE_API_KEY = '640a69fb-68b1-472c-ba4b-36f50288c984'


class wwe_network:

    def __init__(self, user, password):

        with requests.Session() as self._session:
            self._session.headers.update(HEADERS)

        self.user = user
        self.password = password
        self.logged_in = False



    def _set_authentication(self):

        access_token = self.authorisationToken
        if not access_token:
            print("No access token found.")
            return

        self._session.headers.update({'Authorization': 'Bearer {}'.format(access_token)})
        self.logged_in = True

    def login(self):

            payload = {
                "id": self.user,
                "secret": self.password
            }

            token_data = self._session.post('https://dce-frontoffice.imggaming.com/api/v2/login', json=payload, headers=REALM_HEADERS).json()

            if 'code' in token_data:
                print("Error - {}".format(token_data.get('messages')))
                exit()


            self.authorisationToken = token_data['authorisationToken']
            self.refreshToken = token_data['refreshToken']

            self._set_authentication()

    # Get the m3u8 stream
    def m3u8_stream(self, stream_link):

        stream = self._session.get(stream_link, headers=REALM_HEADERS).json()

        return stream['hls']['url']

    def down(self, link):
        return self._session.get(link).content



    def _video_url(self, link):
        video_url = self._session.get('https://dce-frontoffice.imggaming.com/api/v2/stream/vod/{}'.format(link), headers=REALM_HEADERS).json()

        return video_url['playerUrlCallback']

    def get_video_info(self, link):
        api_link = self._session.get('https://cdn.watch.wwe.com/api/page?path=/episode/{}'.format(link)).json()

        return self._video_url(api_link['entries'][0]['item']['customFields']['DiceVideoId']), api_link['entries'][0]['title']
