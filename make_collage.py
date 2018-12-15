import os
import sys
import imageio
from datetime import datetime, timedelta

# Throws an exception if there are no images.
# Creates a gif from images from dir_path starting from from_time. If from_time
# is None, all the files are used.
def make_collage(output_file, dir_path, from_time=None, time_between_frames=1):
	files = [dir_path + '/' + file for file in os.listdir(dir_path)]
	
	if from_time is not None:
		epoch = datetime.utcfromtimestamp(0)
		files = filter(
			lambda f: os.path.getctime(f) > (from_time - epoch).total_seconds(),
			files
		)

	imgs = [imageio.imread(f) for f in files]
	imageio.mimsave(output_file, imgs, duration=time_between_frames)

# python3 make_collage.py out.gif ~/Desktop/gif_test/
if __name__ == '__main__':
	make_collage(
		output_file=sys.argv[1],
		dir_path=sys.argv[2],
		from_time=datetime.now() - timedelta(days=1),
		time_between_frames=0.1
	)