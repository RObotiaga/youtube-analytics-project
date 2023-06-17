import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.name = None
        self.description = None
        self.channel_statistics = None
        self.url = None
        self.sub_count = None
        self.vid_count = None
        self.views_count = None
        self.get_channel_data()
    def __str__(self):
        return f"{self.name} ({self.url})"
    def __add__(self, other):
        return int(self.sub_count) + int(other.sub_count)
    def __sub__(self, other):
        return int(self.sub_count) - int(other.sub_count)
    def __lt__(self, other):
        return int(self.sub_count) < int(other.sub_count)
    def __le__(self, other):
        return int(self.sub_count) <= int(other.sub_count)
    def __gt__(self, other):
        return int(self.sub_count) > int(other.sub_count)
    def __ge__(self, other):
        return int(self.sub_count) >= int(other.sub_count)
    def get_channel_data(self) -> None:
        """Получает информацию о канале и его статистику через API."""
        channel_data = youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()

        if 'items' in channel_data:
            self.name = channel_data['items'][0]['snippet']['title']
            self.description = channel_data['items'][0]['snippet']['description']
            self.channel_statistics = channel_data['items'][0]['statistics']
            self.url = channel_data['items'][0]['snippet']['customUrl']
            self.sub_count = channel_data['items'][0]['statistics']['subscriberCount']
            self.vid_count = channel_data['items'][0]['statistics']['videoCount']
            self.views_count = channel_data['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return youtube

    def to_json(self, file_path: str) -> None:
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        data = {
            'channel_id': self.channel_id,
            'channel_name': self.name,
            'channel_description': self.description,
            'channel_statistics': self.channel_statistics,
            'channel_url': self.url,
            'channel_sub_count': self.sub_count,
            'channel_vid_count': self.vid_count,
            'channel_views_count': self.views_count
        }

        with open(file_path, 'w') as file:
            json.dump(data, file)