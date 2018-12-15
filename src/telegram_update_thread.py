from cmds import CmdManager
from time import sleep
import threading

class TelegramUpdateThread(threading.Thread):
    def __init__(self, bot, ids):
        super().__init__()
        self.bot = bot
        self.ids = ids

    def run(self):
        max_update_id = 0

        while True:
            sleep(0.5)
            for update in self.bot.get_updates(max_update_id + 1):
                max_update_id = max(max_update_id, update.update_id)
                cmd_manager = CmdManager(self.bot, self.ids, update)
                cmd_manager.process_update()