from easysnmp import Session
from typing import Optional

from .constants import *
from .port_status import *

class SNMPManager:
    def __init__(self, hostname: str, community_read: str, community_write: str, version: int):
        self.reader_session = Session(hostname=hostname, community=community_read, version=version)
        self.writer_session = Session(hostname=hostname, community=community_write, version=version)

    def get_port_status(self, port_number: Optional[int] = None) -> list:
        if port_number:
            return self.reader_session.get(IF_OPER_STATUS + '.' + str(port_number))
        return self.reader_session.walk(IF_OPER_STATUS)

    def change_port_status(self, port_number: int, value: PortStatus) -> bool:
        return self.writer_session.set(IF_ADMIN_STATUS + '.' + str(port_number), value, 'i')

    def get_port_numbers(self, mac_address: Optional[str] = None):
        if mac_address:
            return self.reader_session.get(DOT1DTP_FDB_PORT + '.' + mac_address)
        return self.reader_session.walk(DOT1DTP_FDB_PORT)
