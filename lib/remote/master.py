import Pyro4,hmac


key = hmac.new("ServerIlkom")
Pyro4.config.HMAC_KEY = key.hexdigest()

server = Pyro4.Proxy("PYRO:server@192.168.70.254:4000")

def VpsList():
    return server.registered_vps()