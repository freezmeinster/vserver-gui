import Pyro4

info = Pyro4.Proxy("PYRO:VpsInfo@192.168.70.1:4000")

def VpsList():
    return info.getVpsList()