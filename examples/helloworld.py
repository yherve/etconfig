#!/usr/bin/env python
import sys
sys.path.append("..")
import etconfig

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
# now we can use lxml/elementree api (xpath, ...)
res = config.find("network/ip").get("address")
print(res) # 10.20.30.1
