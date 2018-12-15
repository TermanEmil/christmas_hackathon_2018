from PIL import Image
import os
import random
import sys


# Returns the final img with the given frame
def add_frame(img_path, frame_path):
	img = Image.open(img_path, 'r').convert("RGBA")
	frame = Image.open(frame_path, 'r').convert("RGBA")
	frame = frame.resize(img.size)
	final = Image.new('RGBA', img.size)
	final = Image.alpha_composite(final, img)
	final = Image.alpha_composite(final, frame)
	return final

# Picks a random frame from the given dir and adds it to img.
# If the output_path is not given, the img will be overwritten.
def add_random_frame(img_path, output_path=None, frames_dir='./img_frames/'):
	frames = os.listdir(frames_dir)
	frame_path = frames_dir + '/' + random.choice(frames)

	framed_img = add_frame(img_path, frame_path)
	if output_path is None:
		output_path = img_path

	framed_img.save(output_path)

# add_random_frame(sys.argv[1])