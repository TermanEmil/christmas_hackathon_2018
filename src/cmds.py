from photo_ops import send_photo, take_photo
import subprocess
import consts
import random


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