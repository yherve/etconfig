import etconfig

def test_basic():
        MY_CONF="""
        network {
            name="mynet1name"
            forward.mode=nat
            forward.nat.port {start=1024 end=65535}
            ip {
               address=10.20.30.1
               netmask=255.255.255.0
               dhcp.range {start=10.20.30.40 end=10.20.30.254}
            }
        }
"""
        config = etconfig.loads(MY_CONF)
        assert config
        assert config.find("network/ip").get("address") == "10.20.30.1"
