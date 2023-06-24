import os
from googleapiclient.discovery import build

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.name = None
        self.views_count = None
        self.url = None
        self.like_count = None
        self.get_video_data()

    def get_video_data(self):
        """Получает информацию о видео и его статистику через API."""
        video_data = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id
                                           ).execute()
        if 'items' in video_data:
            self.name = video_data['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views_count = video_data['items'][0]['statistics']['viewCount']
            self.like_count = video_data['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name


class PLVideo:
    def __init__(self, video_id, playlist_id):
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.name = None
        self.views_count = None
        self.url = None
        self.like_count = None
        self.get_video_data()

    def get_video_data(self):
        """Получает информацию о видео и его статистику через API."""
        video_data = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id
                                           ).execute()
        if 'items' in video_data:
            self.name = video_data['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views_count = video_data['items'][0]['statistics']['viewCount']
            self.like_count = video_data['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name
