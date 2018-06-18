"""
Small utility to generate video from set of images.
"""

from subprocess import run


__all__ = ['VideoGenerator']


class VideoGenerator:

    @staticmethod
    def run(images_dir_path, output_file_path, frame_rate, frame_size):
        cmd = ['ffmpeg',
               '-y',
               '-pattern_type', 'glob',
               '-i', '%s/*.png' % images_dir_path,
               '-framerate', '%s' % frame_rate,
               '-s:v', '%sx%s' % (frame_size[0], frame_size[1]),
               '-c:v', 'libx264',
               '-profile:v', 'high',
               '-crf', '20',
               '-pix_fmt', 'yuv420p',
               output_file_path]
        run(cmd)
