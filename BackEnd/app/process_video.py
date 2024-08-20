import yt_dlp
import imageio_ffmpeg as ffmpeg
import subprocess
import os

def download_clip(youtube_url, start_time, end_time, save_path="./video_downloads"):
    """ 
    Download a clip from a youtube video and save it to local.

    Args:
        youtube_url : string of the youtube video url to download
        start_time : string of the start time of the clip in the format "MM:SS"
        end_time : string of the end time of the clip in the format "MM:SS"
        save_path (optional): string of the path to save the clip. Default is "./video_downloads".
        
    Returns:
        output_file : string of the path to the saved clip. None if an error occurred.
    """    
    
    try:
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_file = ydl.prepare_filename(info_dict)

        if start_time == "FULL_VIDEO":
            start_time = "00:00"

        if end_time == "FULL_VIDEO":
            end_time = str(info_dict['duration'])

        
        output_file = f"{save_path}/clip_{start_time.replace(':','')}_{end_time.replace(':','')}.mp4"
        ffmpeg_command = [
            ffmpeg.get_ffmpeg_exe(),
            '-y', # overwrite output file if it exists
            '-i', video_file,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',
            output_file
        ]
        subprocess.run(ffmpeg_command, check=True)
        
        print(f"Clip created: {output_file}")
        print(f"Erase the original video file: {video_file}")
        if video_file:
            subprocess.run(["rm", "-rf", video_file])
            
        
        return output_file
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        

def main():
    youtube_url = "https://www.youtube.com/watch?v=06j6X7hEFog"
    start_time = "01:40"
    end_time = "01:47"
    download_clip(youtube_url, start_time, end_time)

if __name__ == "__main__":
    main()