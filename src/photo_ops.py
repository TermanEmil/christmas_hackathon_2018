import subprocess
from datetime import datetime

def take_photo(root_dir='../'):
    time = datetime.now()
    file_name = root_dir + '/' + 'photos/guest{time:%Y%m%d_%H%M%S}.jpg'.format(time=time)

    subprocess.call(['fswebcam', '--no-banner', file_name])
    return file_name

def send_photo(ids, bot, file_name, caption=None):
    for chat_id in ids:
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'), caption=caption)
