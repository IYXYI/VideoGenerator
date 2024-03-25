import os
import instaloader
import moviepy.editor as mp
import shutil






def download_last_2_reels(username):  
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)



    #list of reels 
    reels = []
    # Iterate through the last 2 posts
    for post in profile.get_posts():
        if len(reels) >= 2:
            break
        if post.is_video and post.typename == 'GraphVideo':
            reels.append(post)

    # Download the reels
    if reels:
        # Create a folder for reels if it doesn't exist
        folder_path = 'all_reels'
        os.makedirs(folder_path, exist_ok=True)
        for reel in reels:
            try:
                L.download_post(reel, target=folder_path)
                print(f"Reel {reel.shortcode} downloaded.")
            except FileNotFoundError:
                print(f"File {reel.shortcode}.mp4 not found.")

# List of 5 usernames
usernames = ['chaghab.bdarija', 'amazighia_7orra', 'snapmaroc.officiel1', 'igag_officiel', 'moul.whatsapp']

# Download last 2 reels for each username into one folder
for username in usernames:
    download_last_2_reels(username)

# Create a list to store video file paths
video_files = []

# Iterate through 'all_reels' folder and collect video file paths
folder_path = 'all_reels'
for filename in os.listdir(folder_path):
    if filename.endswith('.mp4'):
        video_files.append(os.path.join(folder_path, filename))

# Create a video using reels from the 'all_reels' folder
if video_files:
    clips = [mp.VideoFileClip(video_file) for video_file in video_files]
    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile('output_video.mp4')
else:
    print("No video files found in 'all_reels' folder.")
