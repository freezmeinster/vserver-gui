import Pyro4,hmac

info = Pyro4.Proxy("PYRO:VpsServer@192.168.70.1:4000")

key = "IlkomUpi"
hmac_key = hmac.new(key)
Pyro4.config.HMAC_KEY = hmac_key.hexdigest()

def VpsList():
    vps = info.vpsserver()
    return vps.get_registered_vps()