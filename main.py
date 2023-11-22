import subprocess


class VideoProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def create_bbb_container(self):
        # FFmpeg command to cut BBB into a 50-second video, export audio as MP3 mono track, MP3 stereo with lower bitrate, and AAC codec
        ffmpeg_bbb_command = [
            'ffmpeg',
            '-i', self.input_file,
            '-t', '50',  # Cut video to 50 seconds
            '-c:v', 'copy',
            '-an', 'bbb_50s_video.mp4',  # Output video file

            '-vn', '-ar', '44100', '-ac', '1', '-b:a', '192k', 'bbb_50s_mono.mp3',  # Export audio as MP3 mono track

            '-vn', '-ar', '44100', '-ac', '2', '-b:a', '128k', 'bbb_50s_stereo.mp3',
            # Export audio as MP3 stereo with lower bitrate

            '-vn', '-c:a', 'aac', '-b:a', '192k', 'bbb_50s_aac.mp4',  # Export audio in AAC codec
            '-strict', 'experimental',
            '-map', '0:v:0', '-map', '1:a:0', self.output_file  # Output MP4 file
            # Map video and audio streams

        ]

    def process_video(self):
        ffmpeg_command = ['ffmpeg',
                          '-flags2',
                          '+export_mvs',
                          '-i', self.input_file,
                          '-vf',
                          'codecview=mv=pf+bf+bb', self.output_file

                          ]

        subprocess.run(ffmpeg_command)

    def create_bbb_container(self):
        # Output file paths
        output_bbb_50s_audio_mono = 'bbb_50s_mono.mp3'
        output_bbb_50s_audio_stereo = 'bbb_50s_stereo.mp3'
        output_bbb_50s_audio_aac = 'bbb_50s_aac.aac'
        output_bbb_container = 'bbb_container.mp4'

        # FFmpeg commands for each requirement
        ffmpeg_cut_video = [
            'ffmpeg',
            '-i', self.input_file,
            '-t', '50',
            '-c', 'copy',
            '-map', '0',
            '-map', '0:a',  # Include all audio streams
            output_bbb_container
        ]

        ffmpeg_export_audio_mono = [
            'ffmpeg',
            '-i', output_bbb_container,
            '-vn',
            '-ac', '1',
            '-q:a', '2',
            output_bbb_50s_audio_mono
        ]

        ffmpeg_export_audio_stereo = [
            'ffmpeg',
            '-i', output_bbb_container,
            '-vn',
            '-ac', '2',
            '-b:a', '64k',
            output_bbb_50s_audio_stereo
        ]

        ffmpeg_export_audio_aac = [
            'ffmpeg',
            '-i', output_bbb_container,
            '-vn',
            '-c:a', 'aac',
            '-strict', 'experimental',
            output_bbb_50s_audio_aac
        ]

        # Run FFmpeg commands
        subprocess.run(ffmpeg_cut_video)
        subprocess.run(ffmpeg_export_audio_mono)
        subprocess.run(ffmpeg_export_audio_stereo)
        subprocess.run(ffmpeg_export_audio_aac)

    def count_tracks(self):
        # FFprobe command to get information about the input video
        ffprobe_command = [
            'ffprobe',
            '-v', 'error',
            '-count_frames',
            '-show_entries', 'stream=codec_type',
            '-of', 'compact=p=0:nk=1',
            self.input_file
        ]

        # Run FFprobe command
        result = subprocess.run(ffprobe_command, capture_output=True, text=True)

        if result.returncode == 0:
            # Count the number of audio tracks
            track_count = len(result.stdout.strip().split('\n'))
            print(f'The video contains {track_count} audio tracks.')
        else:
            print(f'Error running ffprobe: {result.stderr}')


# TASK 1 - MACROBLOCKS AND VECTORS

input_video = 'bunny9s.mp4'
output_video = 'bunny9s_macroblocks_vectors.mp4'

processor = VideoProcessor(input_video, output_video)
processor.process_video()
# TASK 2 - CONTAINER

input_bbb_video = 'bunny.mp4'

processor = VideoProcessor(input_bbb_video, output_file=None)
processor.create_bbb_container()

# TASK 3 - CONTAINER'S TRACKS COUNTER

print('Task 3 - Container track counter')

processor = VideoProcessor('bbb_container.mp4', output_file=None)
processor.count_tracks()

# TASK 4/5- SUBTITLES INHERITANCE

from subtitles import integrate_subtitles

input_video = 'bunny.mp4'
output_video_with_subtitles = 'output_video_with_subtitles.mp4'
subtitles_url = 'https://github.com/moust/MediaPlayer/blob/master/demo/subtitles.srt'

integrate_subtitles(input_video, output_video_with_subtitles, subtitles_url)

# TASK 6 - YUV INHERITANCE

from yuv import extract_yuv_histogram

input_video = 'bunny.mp4'
histogram_video = 'histogram_video.mp4'

extract_yuv_histogram(input_video, histogram_video)
