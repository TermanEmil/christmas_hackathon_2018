import subprocess
import consts
import os
from datetime import datetime
from add_frame import add_random_frame


def take_photo():
    time = datetime.now()
    file_name = consts.photos_dir + '/guest{time:%Y%m%d_%H%M%S}.jpg'.format(time=time)

    subprocess.call(['fswebcam', '--no-banner', file_name])
    if consts.add_frame:
        modified_file = file_name.replace('.jpg', '.png')
        add_random_frame(file_name, frames_dir=consts.frames_dir, output_path=modified_file)

        os.remove(file_name)
        file_name = modified_file
    return file_name

def send_photo(ids, bot, file_name, caption=None):
    for chat_id in ids:
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'), caption=caption)

def send_gif(ids, bot, file_name):
    for chat_id in ids:
        bot.send_animation(chat_id=chat_id, animation=open(file_name, 'rb'))