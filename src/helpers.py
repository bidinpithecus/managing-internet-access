from getmac import get_mac_address as gma

def get_mac_address() -> str | None:
    mac = gma()
    if mac:
        mac = mac.split(':')
    else:
        return mac

    return '.'.join(map(lambda x : str(int(x, 16)), mac))
