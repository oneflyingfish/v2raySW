import base64
import json
from urllib.parse import unquote

class ProxyType:
    unknown=0
    vmess=1
    trojan=2

class ProxyUrl:
    def __init__(self):
        self.name=None
        self.url=None
        self.type=ProxyType.unknown
        self.url_dict=None
        self.tag=None
        self.valid=False
        self.hash=None

    def Hash(self)->str:
        if not self.valid:
            return None
        
        if self.hash is not None:
            return self.hash

        value = hash(str(self.ToList()))
        if value>=0:
            self.hash = "0"+str(abs(value))
        else:
            self.hash = "1"+str(abs(value))

        return self.hash

    def Load(self):
        pass

    def ToList(self):
        return [self.name, self.url, self.tag, self.valid]

    def GetXrayConfig(self)->dict:
        print("you call in-valid ProxyUrl")
        return {}


class VmessProxyUrl(ProxyUrl):
    def __init__(self):
        super().__init__()
        self.type=ProxyType.vmess

    def Load(self, url:str):
        try:
            self.tag = json.loads(base64.b64decode(url.split("://")[1]).decode("utf-8"))
            self.name=self.tag["ps"]

            host = self.tag["add"]
            port = self.tag["port"]
            id = self.tag["id"]
            aid = self.tag["aid"]
            path = self.tag["path"]
            tls = self.tag["tls"]
            net = self.tag["net"]
            type = self.tag["type"]
            self.url=f"vmess://{id}:{aid}@{host}:{port}/?path={path}&tls={tls}&net={net}&type={type}"
            
            self.url_dict={}
            self.url_dict["address"]=host
            self.url_dict["port"]=port
            self.url_dict["id"]=id
            self.url_dict["alterId"]=aid
            self.url_dict["path"]=path
            self.valid=True
        except:
            self.valid=False

    def GetXrayConfig(self)->dict:
        config_dict = dict()
        config_dict["tag"] = "proxy"
        config_dict["protocol"] = "vmess"
        config_dict["settings"] = {
            "vnext": [
                {
                    "address": self.url_dict["address"],
                    "port": self.url_dict["port"],
                    "users": [
                        {
                            "id": self.url_dict["id"],
                            "alterId": self.url_dict["alterId"],
                            "email": "t@t.tt",
                            "security": "auto",
                        }
                    ],
                }
            ]
        }
        if self.url_dict["path"] == "/":
            config_dict["streamSettings"] = {
                "network": "ws",
                "wsSettings": {
                    "path": "/",
                    "headers": {
                        "Host": "25a22a928d882c4614d03a2d3135280e.mobgslb.tbcache.com"
                    },
                },
            }
        else:
            config_dict["streamSettings"] = {
                "network": "ws",
                "wsSettings": {"headers": {}},
            }
        config_dict["mux"] = {"enabled": False, "concurrency": -1}
        return config_dict

class TrojanProxyUrl(ProxyUrl):
    def __init__(self):
        super().__init__()
        self.type=ProxyType.trojan

    def Load(self, url:str):
        try:
            self.name = unquote(url.split("#")[1].split("\r")[0])
            self.url = url.split("#")[0]
            self.tag = url

            self.url_dict={}
            self.url_dict["address"] = self.url.split("@")[1].split(":")[0]
            self.url_dict["port"] = int(self.url.split("@")[1].split(":")[1].split("?")[0])
            self.url_dict["password"] = self.url.split("@")[0].split("//")[1]

            self.valid=True
        except:
            self.valid=False

    def GetXrayConfig(self)->dict:
        config_dict ={}
        config_dict["tag"] = "proxy"
        config_dict["protocol"] = "trojan"
        config_dict["settings"] = {
            "servers": [
                {
                    "address": self.url_dict["address"],
                    "method": "chacha20",
                    "ota": False,
                    "password": self.url_dict["password"],
                    "port": self.url_dict["port"],
                    "level": 1,
                    "flow": "",
                }
            ]
        }
        config_dict["streamSettings"] = {
            "network": "tcp",
            "security": "tls",
            "tlsSettings": {
                "allowInsecure": False,
                "serverName": self.url_dict["address"],
                "show": False,
            },
        }
        config_dict["mux"] = {"enabled": False, "concurrency": -1}
        return config_dict