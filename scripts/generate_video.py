import cv2
import os


# Arguments
images_dir_path = 'D:\\Dev\\Bf\\images\\000073'  # Image directory
output_file_path = 'D:\\Dev\\Bf\\images\\000073.mp4'
frame_rate = 10  # video framerate

# Get the files from directory
images = os.listdir(images_dir_path)
images.sort()

# Determine the width and height from the first image
image_path = os.path.join(images_dir_path, images[0])
frame = cv2.imread(image_path)
height, width, channels = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'h264')
writer = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (730, 730))  # 0x00000021

for n, image in enumerate(images):
    image_path = os.path.join(images_dir_path, image)
    image_size = os.path.getsize(image_path)
    frame = cv2.imread(image_path)
    writer.write(frame)  # Write out frame to video

# Release everything if job is finished
writer.release()
cv2.destroyAllWindows()
