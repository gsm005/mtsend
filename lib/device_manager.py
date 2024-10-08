import globals
from globals import mprint
from models.device import Device, DeviceType
from models.event_type import EventType
import time
import threading
import queue

class DeviceManager():
    def __init__(self):
        self.devices: dict[str, Device] = {}
    
    def add_device(self, ip, name, admin=False):
        if ip not in self.devices:
            mprint(f'New device {name} has joined')
            globals.service_queue.put({'type': EventType.DEVICES_UPDATED})
        if admin:
            self.devices[ip] = Device(ip, name, DeviceType.ADMIN, time.time())
        else:
            self.devices[ip] = Device(ip, name, DeviceType.CLIENT, time.time())
    
    def remove_device(self, ip: str):
        mprint(f'Device {self.devices[ip].name} has left')
        globals.service_queue.put({'type': EventType.DEVICES_UPDATED})
        del self.devices[ip]
    
    def is_empty(self):
        return len(self.devices) == 0
    
    def get_devices(self):
        return self.devices.values()
    
    def device_updater(self, ip, name):
        if ip in self.devices:
            self.devices[ip].name = name
            self.devices[ip].last_seen = time.time()
        else:
            self.add_device(ip, name)
    
    def device_remove_listener(self):
        while True:
            for device in list(self.devices.values()):
                if time.time() - device.last_seen > globals.DEVICE_ONLINE_TIMEOUT*1.1:
                    self.remove_device(device.ip)
    
    def start(self):
        device_remove_thread = threading.Thread(target=self.device_remove_listener, daemon=True)
        device_remove_thread.start()
    
    def close(self):
        self.on = False
        globals.mprint('DeviceManager has been closed')