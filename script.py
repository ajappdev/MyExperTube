from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


# API key obtained from the Google Developers Console
API_KEY = "AIzaSyBi3D9Qh7zimeMcUBJiNOMsbKUIeTGgPuo"


# DECLARING FUNCTIONS
def extract_handle(channel_url: str):
    """
    This function takes youtube channel urls and extract the username
    (or handle) of the channel
    """
    # Split the URL by '/'
    parts = channel_url.split('/')

    # Find the part containing the handle
    for part in parts:
        if part.startswith('@'):
            return part[1:]  # Remove the '@' prefix

    return None


def get_channel_id(channel_url: str):
    """
    This function takes the channel url and give the channel ID
    """
    channel_handle = extract_handle(channel_url)
    # Construct the URL
    url = f"https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&forHandle={channel_handle}&part=id"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the channel ID URL
        if 'items' in data and data['items']:
            channel_id_url = data['items'][0]['id']
            return channel_id_url

    # If the request was unsuccessful or channel ID URL not found, return None
    return None



def get_channel_videos(channel_url: str):
    """
    This function takes the channel_url and returns a list of IDs of all
    videos in the channel
    """
    # YouTube channel ID
    channel_id = get_channel_id(channel_url)
    if channel_id:
        video_ids = []

        possible_orders = ['date', 'rating', 'relevance', 'title', 'viewCount']
        for order in possible_orders:
            url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order={order}&maxResults=50"
            # Make the GET request
            response = requests.get(url)
            # Initialize the YouTube Data API
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                # Extract the channel ID URL
                if 'items' in data and data['items']:
                    for item in data['items']:
                        if 'videoId' in item['id']:
                            video_id = item['id']['videoId']
                            video_ids.append(video_id)
        return list(set(video_ids))
        
    else:
        print("Channel ID not found.")


def get_video_captions(video_id: str):
    """
    
    """
    video_captions = YouTubeTranscriptApi.get_transcript(video_id)
    return video_captions


def get_channel_content(channel_url: str):
    """
    
    """
    channel_videos = get_channel_videos(channel_url)

    # List to store captions
    captions = []

    # Retrieve captions for each video
    for video_id in channel_videos:
        print(video_id)
        video_captions = get_video_captions(video_id)
        captions.extend(video_captions)

    # Write captions to a text file
    with open('captions.txt', 'w', encoding='utf-8') as file:
        for caption in captions:
            file.write(caption['text'] + '\n')
    
    print("Captions saved to captions.txt")


get_channel_videos('https://www.youtube.com/@HighValueMen')