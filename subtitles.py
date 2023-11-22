import requests
import subprocess


def download_subtitles(subtitles_url):
    # Download subtitles file
    response = requests.get(subtitles_url)

    print(f'Status Code: {response.status_code}')
    print(f'Content: {response.content}')

    if response.status_code == 200:
        subtitles_file_path = 'downloaded_subtitles.srt'
        with open(subtitles_file_path, 'wb') as subtitles_file:
            subtitles_file.write(response.content)
        return subtitles_file_path
    else:
        print(f'Error downloading subtitles. Status code: {response.status_code}')
        return None


def integrate_subtitles(input_file, output_file, subtitles_url):
    # Download subtitles
    subtitles_file = download_subtitles(subtitles_url)

    if subtitles_file:
        # FFmpeg command to integrate subtitles into the video
        ffmpeg_integrate_subtitles = [
            'ffmpeg',
            '-i', input_file,
            '-i', subtitles_file,
            '-c', 'copy',
            '-c:s', 'mov_text',
            '-map', '0',
            '-map', '1',
            output_file
        ]

        print("FFmpeg command:", ' '.join(ffmpeg_integrate_subtitles))  # Print FFmpeg command for debugging

        try:
            # Run FFmpeg command to integrate subtitles
            result = subprocess.run(ffmpeg_integrate_subtitles, capture_output=True, text=True)
        except Exception as e:
            print(f'Exception during FFmpeg execution: {e}')
            return

        print(f'FFmpeg output: {result.stdout}')
        print(f'FFmpeg error output: {result.stderr}')

        if result.returncode == 0:
            print("Subtitles integrated successfully.")
        else:
            print(f'Error integrating subtitles. FFmpeg output: {result.stderr}')



