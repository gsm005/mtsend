from enum import Enum

class PacketType(Enum):
    ONLINE = 0
    OFFLINE = 1

    GROUP_JOIN_REQ = 10
    GROUP_JOIN_ACK = 11
    GROUP_LEAVE_REQ = 12
    GROUP_LEAVE_ACK = 13

    GROUP_INFO = 20
    GROUP_MESSAGE = 21
    GROUP_TEXT_MESSAGE = 22
    
    GROUP_FILE_MESSAGE = 30
    GROUP_FILE_CHUNK = 31