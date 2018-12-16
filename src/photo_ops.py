import subprocess
import consts
from datetime import datetime
from add_frame import add_random_frame


def take_photo(root_dir='../'):
    time = datetime.now()
    file_name = root_dir + '/' + 'photos/guest{time:%Y%m%d_%H%M%S}.jpg'.format(time=time)

    subprocess.call(['fswebcam', '--no-banner', file_name])
    if consts.add_frame:
        modified_file = file_name.replace('.jpg', '.png')
        add_random_frame(file_name, frames_dir=consts.frames_dir, output_path=modified_file)
        file_name = modified_file
    return file_name

def send_photo(ids, bot, file_name, caption=None):
    for chat_id in ids:
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'), caption=caption)
