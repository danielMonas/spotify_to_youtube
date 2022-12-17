# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import googleapiclient.discovery as googleapi
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

from log import logger


class YoutubeInterface:
    CREDS_FILE = 'creds.pickle'
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, playlist_id: str) -> None:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.playlist_id = playlist_id
        self.api = self.setup_youtube_api_by_oauth()
        

    def setup_youtube_api_by_oauth(self) -> googleapi.Resource:
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        scopes = ["https://www.googleapis.com/auth/youtube"]
        client_secrets_file = "creds.json"

        if os.path.exists(self.CREDS_FILE):
            with open(self.CREDS_FILE, 'rb') as f:
                credentials = pickle.load(f)
        else:
            # Get credentials and create an API client
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_console()
            with open(self.CREDS_FILE, 'wb') as f:
                pickle.dump(credentials, f)
        youtube_api = googleapi.build(self.API_SERVICE_NAME, self.API_VERSION,
                                      credentials=credentials)
        return youtube_api

    def search_video(self, query: str) -> dict:
        request = self.api.search().list(part="snippet", maxResults=1, q=query)
        response = request.execute()
        logger.debug(f'Got Youtube API response: {response}')
        video = response['items'][0]
        video_id = video.get('id', {})
        return video_id

    def save_to_playlist(self, video_id: str) -> None:
        request = self.api.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": self.playlist_id,
                    "position": 0,
                    "resourceId": {
                      "kind": "youtube#video",
                      "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        logger.debug(f'Got Youtube API response: {response}')
