import tempfile
import os
import requests
import shutil
from datetime import datetime, timedelta
from moviepy.editor import VideoFileClip, concatenate_videoclips

def _sort_clips_chronologically(clips):
    clips.sort(key=lambda k : k["created_at"])


def _sort_clips_popularity(clips):
    clips.sort(key=lambda k : k["view_count"])


def _merge_videos(clip_list, output_name):
    merged_video = concatenate_videoclips(clip_list, method="compose")

    merged_video.write_videofile(
            f"{output_name}.mp4",
            codec="libx264",
            fps=60,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            audio_codec="aac")

    merged_video.close() 
    for clip in clip_list:
        clip.close()
    

class TwitchHighlights:
    _TWITCH_OAUTH_ENDPOINT = "https://id.twitch.tv/oauth2/token"
    _TWITCH_CLIPS_ENDPOINT = "https://api.twitch.tv/helix/clips"
    _TWITCH_CATEGORY_ENDPOINT = "https://api.twitch.tv/helix/search/categories"
    _TWITCH_TOP_GAMES_ENDPOINT = "https://api.twitch.tv/helix/games/top"
    _TWITCH_BROADCASTER_ENDPOINT = "https://api.twitch.tv/helix/users"


    def __init__(self, twitch_credentials = None):
        self.tmpdir = tempfile.TemporaryDirectory()

        if(twitch_credentials):
            self.login_twitch(twitch_credentials)   


    def login_twitch(self, twitch_credentials):
        twitch_client_id = twitch_credentials["client_id"]
        twitch_client_secret =  twitch_credentials["client_secret"]
        query_parameters = f'?client_id={twitch_client_id}&client_secret={twitch_client_secret}&grant_type=client_credentials'

        response = requests.post(self._TWITCH_OAUTH_ENDPOINT + query_parameters)
        twitch_token = response.json()['access_token']

        self.twitch_oauth_header = {"Client-ID": twitch_client_id,
                                    "Authorization": f"Bearer {twitch_token}"}


    def get_top_categories(self, amount = 20):
        categories_json = self._get_request(self._TWITCH_TOP_GAMES_ENDPOINT, f"?first={amount}")
        categories = []

        for category in categories_json:
            categories.append(category['name'])

        return categories    


    def make_video_by_category(self, category, output_name = "output_video", language = None, video_length = 300, started_at = datetime.utcnow() - timedelta(days=1), ended_at = datetime.utcnow(), target_resolution=(1080,1920)):
        clips = self._get_clips_by_category(category, started_at, ended_at)
        self._create_video_from_json(clips, output_name, language, video_length, target_resolution)


    def make_video_by_streamer(self, streamers, output_name = "output_video", language = None, video_length = 300, started_at = datetime.utcnow() - timedelta(days=1), ended_at = datetime.utcnow(), target_resolution=(1080,1920)):
        clips = []

        for streamer in streamers:
            clips += self._get_clips_by_streamer(streamer, started_at, ended_at)

        _sort_clips_popularity(clips)
        self._create_video_from_json(clips, output_name, language, video_length, target_resolution)


    def _create_video_from_json(self, clips, output_name, language, video_length, target_resolution):
        print("Succesfully fetched clip data") 
        self._preprocess_clips(clips, language)

        clip_list = []
        combined_length = 0

        with requests.Session() as s:
            for i, clip in enumerate(clips):
                if combined_length >= video_length:
                    break
                
                print(f'Downloading clip: {clip["broadcaster_name"]} - {clip["title"]}')
                file_path = self._download_clip(s, clip, i)
                newVideoFileClip = VideoFileClip(file_path, target_resolution=target_resolution)
                clip_list.append(newVideoFileClip)
                combined_length += newVideoFileClip.duration

        _merge_videos(clip_list, output_name)
        
        for file in os.listdir(self.tmpdir.name):
            os.remove(os.path.join(self.tmpdir.name, file))


    def _check_twitch_authentication(self):
        if not hasattr(self, "twitch_oauth_header"):
            raise Exception("Twitch authentication incomplete. Please authenticate using the login() method.")


    def _get_request(self, endpoint_url, query_parameters, error_message = "An error occurred"):
        self._check_twitch_authentication()

        response = requests.get(endpoint_url + query_parameters, headers=self.twitch_oauth_header)
        
        if response.json()["data"] == None:
            raise Exception(error_message)

        return response.json()["data"]


    def _preprocess_clips(self, clips, language):
        for clip in clips:
            video_url = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
            clip["video_url"] = video_url

        if language is not None:
            return [clip for clip in clips if language in clip["language"]]
        
        return clips


    def _download_clip(self, session, clip, id):
        if not hasattr(self, "tmpdir"):
            raise Exception("No temporary file storage available for downloaded clips.")

        video_url = clip["video_url"]

        file_path = f'{self.tmpdir.name}/{id}.mp4'

        r=session.get(video_url)
        f=open(file_path,'wb')
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
        f.close()

        return file_path


    def _get_category_id(self, category_name):
        query_parameters = f'?query={category_name}'
        error_message = f'Twitch category not found: "{category_name}"'
        category_list = self._get_request(self._TWITCH_CATEGORY_ENDPOINT, query_parameters, error_message)        
        found_category = next((category for category in category_list if category["name"].lower() == category_name.lower()), None)
        
        if found_category is None:
            raise Exception(f'Category with name "{category_name}" not found.')

        return found_category["id"]


    def _get_broadcaster_id(self, broadcaster_name):        
        query_parameters = f'?login={broadcaster_name}'
        broadcaster_data = self._get_request(self._TWITCH_BROADCASTER_ENDPOINT, query_parameters)
        if len(broadcaster_data) == 0:
            raise Exception(f'Broadcaster with name "{broadcaster_name}" not found.')
        
        return broadcaster_data[0]["id"]


    def _get_clips_by_category(self, category_name, started_at, ended_at):
        started_at = started_at.isoformat("T") + "Z"
        ended_at = ended_at.isoformat("T") + "Z"
        category_id = self._get_category_id(category_name)
        query_parameters = f'?game_id={category_id}&first=100&started_at={started_at}&ended_at={ended_at}'
        return self._get_request(self._TWITCH_CLIPS_ENDPOINT, query_parameters)


    def _get_clips_by_streamer(self, streamer_name, started_at, ended_at):
        started_at = started_at.isoformat("T") + "Z"
        ended_at = ended_at.isoformat("T") + "Z"
        broadcaster_id = self._get_broadcaster_id(streamer_name)
        query_parameters = f'?broadcaster_id={broadcaster_id}&first=100&started_at={started_at}&ended_at={ended_at}'
        
        return self._get_request(self._TWITCH_CLIPS_ENDPOINT, query_parameters)