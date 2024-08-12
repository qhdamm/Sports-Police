import yt_dlp

def download_video(youtube_url, save_path="."):
    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'best',  
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print("Download completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

youtube_url = "https://www.youtube.com/watch?v=BIqt5gEL_U8"
download_video(youtube_url, save_path="./downloads")
