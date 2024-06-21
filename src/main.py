from constants import *
from easysnmp import Session
from getmac import get_mac_address as gma

def change_port_status(writable_session: Session, port_number: int, value: int) -> bool:
    return writable_session.set(IF_ADMIN_STATUS + '.' + str(port_number), value, 'i')

def get_ports_status(readable_session: Session, port_number: int | None = None):
    if port_number:
        return readable_session.get(IF_OPER_STATUS + '.' + str(port_number))

    return readable_session.walk(IF_OPER_STATUS)

def get_ports_numbers(readable_session: Session, mac_address: str | None = None):
    if mac_address:
        return readable_session.get(DOT1DTP_FDB_PORT + '.' + mac_address)

    return readable_session.walk(DOT1DTP_FDB_PORT)

def get_mac_address() -> str:
    mac = gma().split(':')
    mac = '.'.join(map(lambda x : str(int(x, 16)), mac))

reader_session = Session(hostname = HOSTNAME, community = COMMUNITY_READ_NAME, version = SNMP_VERSION)
writer_session = Session(hostname = HOSTNAME, community = COMMUNITY_WRITE_NAME, version = SNMP_VERSION)

'''
-> discover teacher computer mac ---> OK!
-> snmpwalk -v1 -c public 10.90.90.90 .1.3.6.1.2.1.17.4.3.1.1 | grep mac
    .1.3.6.1.2.1.17.4.3.1.1.108.60.140.70.132.108 = Hex-STRING: 6C 3C 8C 46 84 6C ---> NOT NECESSARY ---> Already converting it to decimal 
-> after, .1.3.6.1.2.1.17.4.3.1.1. in OID is the decimal representation of mac, i.e. 108.60.140.70.132.108
-> to get the switch port number: snmpget host .1.3.6.1.2.1.17.4.3.1.2.++decimal_mac

-> to guess the link port, perform a walk in OID: .1.3.6.1.2.1.17.4.3.1.2, and set it to the maximum occurrence port.
'''
