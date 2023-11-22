import subprocess


def extract_yuv_histogram(input_file, output_file):
    # we extract YUV histogram using ffmpeg
    extract_command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'colorbalance=rs=0.2:gs=0.2:bs=0.2',
        '-c:v', 'libx264',
        '-crf', '20',
        '-c:a', 'copy',
        output_file
    ]
    subprocess.run(extract_command, check=True)
