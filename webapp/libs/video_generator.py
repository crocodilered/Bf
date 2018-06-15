"""
Small utility to generate video from set of images.
"""

import cv2
import os


__all__ = ['VideoGenerator']


class VideoGenerator:

    @staticmethod
    def run(images_dir_path, output_file_path, frame_rate, frame_size):
        # Remove output file
        if os.path.isfile(output_file_path):
            os.remove(output_file_path)

        # Get the files from directory
        images = os.listdir(images_dir_path)
        images.sort()

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'h264')
        writer = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (730, 730))  # 0x00000021

        for n, image in enumerate(images):
            image_path = os.path.join(images_dir_path, image)
            frame = cv2.imread(image_path)
            writer.write(frame)  # Write out frame to video

        # Release everything if job is finished
        writer.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # test
    images_dir_path = 'D:\\Dev\\Bf\\images\\000073'
    output_file_path = 'D:\\Dev\\Bf\\images\\000073.mp4'
    frame_rate = 10
    frame_size = (710, 710)
    VideoGenerator.run(images_dir_path, output_file_path, frame_rate, frame_size)
