from photo_ops import send_photo, send_gif, take_photo
from telegram import ChatAction
from make_collage import make_collage
from datetime import datetime, timedelta
import re
import subprocess
import consts
import random
import os


class CmdManager:
    def __init__(self, bot, ids, update):
        self.bot = bot
        self.ids = ids
        self.update = update

    def process_update(self):
        if not self.update.message.text:
            return

        cmd_name, *_ = self.update.message.text.partition(' ')
        if cmd_name == '/start' and not self.update.message.chat_id in self.ids:
            self.cmd_start()

        elif self.update.message.chat_id in self.ids:
            if cmd_name == '/stop':
                self.cmd_stop()               
            elif cmd_name == '/send':
                self.cmd_send()            
            elif cmd_name == '/photo':
                self.cmd_take_photo()
            elif cmd_name == '/collage':
                self.cmd_make_collage()

    def chat_id(self):
        return self.update.message.chat_id

    def cmd_start(self):
        self.ids.add(self.chat_id())
        self.bot.send_message(chat_id = self.chat_id(), text = "Waiting for Santa")

    def cmd_stop(self):
        self.ids.remove(self.chat_id())
        self.bot.send_message(chat_id = self.chat_id(), text = "But... you will miss Santa.... :(")

    def cmd_send(self):
        *_, text_to_send = self.update.message.text.partition(' ')
        text_to_send = text_to_send[:16] + '\n' + text_to_send[16:32]
        subprocess.call(["python3", "lcd.py", text_to_send])
        self.bot.send_message(chat_id = self.chat_id(), text = "Msg has been sent")

    def cmd_take_photo(self):
        for chat_id in self.ids:
            self.bot.send_chat_action(chat_id, 'upload_photo')

        photo = take_photo()
        send_photo(self.ids, self.bot, photo)

    def cmd_make_collage(self):
        for chat_id in self.ids:
            self.bot.send_chat_action(chat_id, ChatAction.TYPING)
        
        if not os.path.exists(consts.collages_dir):
            os.makedirs(consts.collages_dir)
        
        time = datetime.now()
        file_name = consts.collages_dir + '/collage_{time:%Y%m%d_%H%M%S}.gif'.format(time=time)

        # /collage time=30
        argv = self.update.message.text.split()
        from_time_in_mins = consts.from_time_in_mins

        try:
            if len(argv) == 2:
                regex = r'time=(\d+)'
                match = re.match(regex, argv[1])            
                
                if match:
                    from_time_in_mins = int(match.group(1))
        except:
            pass
        
        try:
            make_collage(
                file_name,
                consts.photos_dir,
                from_time=datetime.now() - timedelta(minutes=from_time_in_mins),
                time_between_frames=consts.time_between_frames)
        except RuntimeError:
            self.bot.send_message(chat_id = self.chat_id(), text = "Failed to make a collage. No photos currently available.")
            return
        
        print('-------', file_name)
        send_gif(self.ids, self.bot, file_name)
        