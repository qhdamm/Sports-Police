import yt_dlp
import imageio_ffmpeg as ffmpeg
import subprocess

def download_clip(youtube_url, start_time, end_time, save_path="."):
    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_file = ydl.prepare_filename(info_dict)
        output_file = f"{save_path}/clip_{start_time.replace(':','')}_{end_time.replace(':','')}.mp4"
        ffmpeg_command = [
            ffmpeg.get_ffmpeg_exe(),
            '-i', video_file,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',
            output_file
        ]
        subprocess.run(ffmpeg_command, check=True)
        
        print(f"Clip created: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

youtube_url = "https://www.youtube.com/watch?v=06j6X7hEFog"
start_time = "01:40"
end_time = "01:47"
download_clip(youtube_url, start_time, end_time, save_path="./downloads")
