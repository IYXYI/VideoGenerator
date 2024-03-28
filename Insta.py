import moviepy.editor as mp
from pytube import Search

def download_youtube_videos_with_hashtag(hashtag, max_duration=20, max_videos=2):
    search_query = f"{hashtag}"
    search_results = Search(search_query)

    downloaded_videos = []
    for video in search_results.results[:max_videos]:
        try:
            if video.length <= max_duration:
                downloaded_videos.append(video.streams.get_highest_resolution().download())
                print(f"Downloaded video: {video.title}")
        except Exception as e:
            print(f"Error downloading video: {e}")

    return downloaded_videos

hashtag = "happy"
max_duration = 250
downloaded_videos = download_youtube_videos_with_hashtag(hashtag, max_duration=max_duration, max_videos=2)

if downloaded_videos:
    # Create montage within the loop (after first download)
    montage = None  # Initialize montage as None
    for video_path in downloaded_videos:
        video_clip = mp.VideoFileClip(video_path)
        if montage is None:  # Create montage on first iteration
            montage = mp.CompositeVideoClip([video_clip])
        else:  # Concatenate subsequent clips
            montage = mp.concatenate_videoclips([montage, video_clip])

    final_video_path = f"{hashtag}_montage.mp4"
    montage.write_videofile(final_video_path, fps=24)
    print(f"Montage video created: {final_video_path}")
else:
    print(f"No videos found with hashtag '{hashtag}' and duration less than {max_duration} seconds.")
