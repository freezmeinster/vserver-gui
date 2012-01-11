import Pyro.core
Pyro.core.initClient()
info = Pyro.core.getProxyForURI("PYROLOC://192.168.70.254:4000/server")

def VpsList():
    list = info.get_class()
    return list.get_registered_vps()