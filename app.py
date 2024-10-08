import globals
from globals import mprint
from models.device_type import DeviceType
from admin.admin_ui import AdminUI
from client.client_ui import ClientUI
from lib.main_socket import MainSocket
from lib.device_manager import DeviceManager
from lib.group_manager import GroupManager
from helpers.get_self_ip import get_my_ip
from tkinter import Tk
import queue

class MtSendApplication():
    def __init__(self):
        self.group_manager = GroupManager()
        self.device_manager = DeviceManager()
        self.device_manager.start()
        
        self.main_socket = MainSocket(self.device_manager, self.group_manager)

        self.app_ui: Tk = None
        if globals.DEVICE_TYPE == DeviceType.ADMIN:
            self.app_ui = AdminUI(self.main_socket, self.device_manager, self.group_manager)
        else:
            self.app_ui = ClientUI(self.main_socket, self.device_manager, self.group_manager)

        self.on = True
    
    def run(self):
        mprint('=> You are user', globals.DEVICE_NAME, get_my_ip())
        self.main_socket.start()
        self.app_ui.mainloop()
    
    def __del__(self):
        mprint('MtSendApplication has been closed')