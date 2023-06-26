from googleapiclient.discovery import build
from src.video import Video
import datetime

api_key = 'AIzaSyAbxR8-99iQYeBB26uRYFKi-EORwBFi57E'  # os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.get_playlist_data()

    def get_playlist_data(self):
        playlist_data = youtube.playlists().list(id=self.playlist_id,
                                                 part='snippet',
                                                 maxResults=50,
                                                 ).execute()
        if 'items' in playlist_data:
            self.title = playlist_data['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        duration = 0
        for i in video_ids:
            duration += int(Video(i).duration.total_seconds())
        return datetime.timedelta(seconds=duration)

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_dict = {}
        for i in video_ids:
            video_dict[Video(i).like_count] = Video(i).url
        return video_dict[f'{max(map(int, video_dict.keys()))}']
