from subprocess import run


# Arguments
images_dir_path = 'D:\\Dev\\Bf\\images\\000077'  # Image directory
output_file_path = 'D:\\Dev\\Bf\\images\\000077.mp4'
frame_rate = 10  # video framerate
frame_size_w = 730
frame_size_h = 730

cmd = ['D:\\t\\ffmpeg\\bin\\ffmpeg.exe',
       '-y',
       '-pattern_type', 'glob',
       '-i', '%s/*.png' % images_dir_path,
       '-framerate', '%s' % frame_rate,
       '-s:v', '%sx%s' % (frame_size_w, frame_size_h),
       '-c:v', 'libx264',
       '-profile:v', 'high',
       '-crf', '20',
       '-pix_fmt', 'yuv420p',
       output_file_path]
run(cmd)
